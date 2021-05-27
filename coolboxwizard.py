import coolbox.api as cbx
import coolbox
import yaml
import re, pathlib, collections

load_functions = {'BED': cbx.BED, 
                   'HiCMat': cbx.HiCMat,
                   'TAD_coverage': cbx.TADCoverage,
                   'HiCPeaksCoverage': cbx.HiCPeaksCoverage,
                   'Arcs': cbx.Arcs,
                   'BigWig': cbx.BigWig,
                   'GTF': cbx.GTF,
                   ## TODO ADD MORE FUNCTIONS...
                  }

def load_config(file: str) -> dict:
    '''Loads a YAML config file'''
    fh = open(file, 'r')
    config = yaml.safe_load(fh)
    fh.close()
    
    return config

def get_tracks(config: dict) -> list:
    '''Goes through config YAML file's and returns a list of tracks'''
    coolbox_tracks = []
    
    tracks = config['tracks']
    for track_key in tracks:
        track = tracks[track_key]
        coolbox_tracks += [track]
    return coolbox_tracks

def load_track(track: dict, config: dict) -> coolbox.core.track: # or something else e.g. coolbox.core.coverage.base.TADCoverage 
    '''takes a track info and creates corresponding coolbox track'''
    track_general_params_ = track['track_general_params']
    # print(track_general_params)
    
    if track_general_params_ in config['parameters']:
        track_general_params = config['parameters'][track_general_params_]

    if 'track_general_params' in locals() and track_general_params != None:
        all_params = track_general_params | track # in Python < 3.9 use {**x, **y}; order matters, track params overwrites frame params
    else: 
        all_params = track

    track_type = track['track_type']        
    return load_functions[track_type](**all_params)


def create_frame(file: str) -> coolbox.core.frame.frame.Frame:
    '''Parses a YAML config file and creates coolbox frame from the tracks in the config file'''
    config = load_config(file)
    
    tracks = get_tracks(config)
    
    loaded_tracks = {}
    
    for track in tracks:

        track_order = track['order']

        loaded_tracks[track_order] = load_track(track, config)

    loaded_tracks = collections.OrderedDict(sorted(loaded_tracks.items()))
    
    frame = cbx.XAxis()

    for key in loaded_tracks:
        frame += loaded_tracks[key]
        
    frame += cbx.XAxis()
    
    return frame

def create_yaml_tracks(file_path_iterable: list, offset:int = 0, prefix:str='', suffix:str='', color_map:dict ={}, track_type:str ='', track_general_params_name:str ='', pattern: str='') -> dict:
    '''utility function to create the entries for the YAML config file'''
    
    yaml_dict = {}
    
    for ind, fpath in enumerate(file_path_iterable):
        
        key = '%s_%s' %(prefix, ind)
        
        sample_name = '%s %s' %(pathlib.Path(fpath).stem, suffix)
        
        color_key = re.findall(pattern, sample_name)[0] #XYZ_356 or XYZ356 -> XYZ
        color = color_map[color_key] if color_key in color_map else '#2255ff'
        
        yaml_dict[key] = {'file': fpath,
                          'order': offset + ind + 1, 
                          'title': sample_name,
                          'track_type': '%s' %track_type,
                          'track_general_params': '%s' %track_general_params_name,
                          'color': '#%s' %color,
                          'height': 0.75
                         }
    return yaml_dict