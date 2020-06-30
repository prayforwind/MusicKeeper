import os
import os.path
import pdb
import shutil
import sys
import traceback

import audio_metadata


class AttributeException(Exception):
    """Base exception for audio.metadata."""


def clean_windows_filename(filename):
    invalid = '<>:"/\|?*'
    for char in invalid:
	    filename = filename.replace(char, '')
    filename=filename.encode(encoding='utf-8', errors='ignore').decode(encoding="utf-8", errors="strict")
    return filename
    
class Context(object):
    def __init__(self):
        self.ofs = sys.stdout
        self.efs = sys.stderr
        self.basepath = None
        self.dirpath_filter = None
        self.filename_filter = None
        self.filepath_filter = None
    
    def generate(self, ctx, dirpath, filename, filepath):
        try:
            amd = audio_metadata.load(filepath)
            if not hasattr(amd, 'tags'):
                raise AttributeException("attribute tags missing")
            if not hasattr(amd.tags, 'artist'):
                raise AttributeException("attribute artist missing")
            if not hasattr(amd.tags, 'title'):
                raise AttributeException("attribute title missing")
            new_filename = ('-'.join(amd.tags.artist) + '_' + '-'.join(amd.tags.title)).strip() + os.path.splitext(filename)[1]
            new_filename = clean_windows_filename(new_filename)
            line = new_filename + ' | ' + filepath + '\n'
            ctx.ofs.write(line)
            dest_filepath = os.path.join(ctx.destpath, new_filename)
            if os.path.exists(dest_filepath):
                if os.stat(filepath).st_size <= os.stat(dest_filepath).st_size:
                    return
            shutil.copyfile(filepath, dest_filepath)
        except audio_metadata.AudioMetadataException as e:
            self.error(filepath, e)
        except ValueError as e:
            self.error(filepath, e)
        except AttributeException as e:
            self.error(filepath, e)
        except OSError as e:
            self.error(filepath, e)
        except Exception as e:
            self.error(filepath, e)
        except:
            self.error(filepath, traceback.format_exc())

    def error(self, filepath, e):
        self.efs.write(filepath)
        self.efs.write(' : ')
        self.efs.write(str(e))
        self.efs.write('\n')

def scan(ctx):
    for (dirpath, dirnames, filenames) in os.walk(ctx.basepath):
        if ctx.dirpath_filter(dirpath):
            for filename in filenames:
                if ctx.filename_filter(filename):
                    filepath = os.path.join(dirpath, filename)
                    if ctx.filepath_filter(filepath):
                        ctx.generate(ctx, dirpath, filename, filepath)

class Filter:
    @staticmethod
    def dirpath_filter(dirpath):
        for i in ['album', 'classic', 'broken']:
            if i in dirpath:
                return False
        return True

    @staticmethod
    def filename_filter(filename):
        ext = os.path.splitext(filename)[1]
        if ext in ['.JPG', '.m4a', '.jpg']:
            return False
        return True

    @staticmethod
    def filepath_filter(filepath):
        fz = os.stat(filepath).st_size
        if fz < 1024 * 1024 * 2 or fz > 1024 * 1024 * 1024:
            return False
        return True

def main():
    ctx = Context()
    ctx.basepath = 'C:\\Users\\Neo Martin\\Music'
    ctx.destpath = 'H:\\Music'
    ctx.manifest_name = '_manifest.txt'
    ctx.error_name = '_error.txt'
    ctx.dirpath_filter = Filter.dirpath_filter
    ctx.filename_filter = Filter.filename_filter
    ctx.filepath_filter = Filter.filepath_filter
    with open(os.path.join(ctx.destpath, ctx.manifest_name), 'w', encoding='utf-8') as fo, \
        open(os.path.join(ctx.destpath, ctx.error_name), 'w', encoding='utf-8') as fe:
        ctx.ofs = fo
        ctx.efs = fe
        scan(ctx)

if __name__ == '__main__':
    main()
