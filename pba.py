from render_usd import UsdRenderer

import igl
import os

def load_pba_simulation_eager(path: str):

    filenames = os.listdir(path)
    files = [None]*len(filenames)
    for i, filename in enumerate(filenames):
        tokens = filename.split('.')
        frame, entity = int(tokens[-3]), int(tokens[-2])
        V, F = igl.read_triangle_mesh(os.path.join(path, filename))
        files[i] = (frame, entity, V, F)

    nframes = max(files, key = lambda x: x[0])[0] + 1
    files = sorted(files, key = lambda x: (x[0], x[1]))
    frames = [{} for _ in range(nframes)]
    for (frame, entity, V, F) in files:
        frames[frame]["Entity{}".format(entity)] = (V, F)

    return frames

def load_pba_simulation_lazy(path: str):
    filenames = os.listdir(path)
    files = [None]*len(filenames)
    for i, filename in enumerate(filenames):
        tokens = filename.split('.')
        frame, entity = int(tokens[-3]), int(tokens[-2])
        files[i] = (frame, entity, os.path.join(path, filename))

    nframes = max(files, key = lambda x: x[0])[0]
    files = sorted(files, key = lambda x: (x[0], x[1]))
    frames = [{} for _ in range(nframes)]
    for (frame, entity, filepath) in files:
        frames[frame]["Entity{}".format(entity)] = filepath

    return frames

def render_pba_simulation_to_usd(renderer: UsdRenderer, folder: str, lazy: bool, fps: int):
    if not lazy:
        frames = load_pba_simulation_eager(folder)
        dt = 1.0 / fps
        time = 0.0
        for entities in frames:
            time += dt
            renderer.begin_frame(time)
            for entity_id in entities.keys():
                V, F = entities[entity_id]
                renderer.render_mesh(entity_id, V, F, update_topology=True)
            renderer.end_frame()
    else:
        frames = load_pba_simulation_eager(folder)
        dt = 1.0 / fps
        time = 0.0
        for entities in frames:
            time += dt
            renderer.begin_frame(time)
            for entity_id in entities.keys():
                filepath = entities[entity_id]
                V, F = igl.read_triangle_mesh(filepath)
                renderer.render_mesh(entity_id, V, F, update_topology=True)
            renderer.end_frame()