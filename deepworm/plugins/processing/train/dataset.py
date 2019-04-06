import shutil
import random
from datetime import datetime
import os,sys
sys.path.append('../../../')
from utils.get_parent_path import get_parent_path
import json

class Dataset(object):
    """docstring for Dataset."""

    def __init__(self):
        super(Dataset, self).__init__()
        self.img_dir=''
        self.annotation_path=''
        self.temp_dir=''
        self.destination_dir=''
        self.bundle_dir=get_parent_path(4)
        self.dataset={}

    def make_temp_dir(self):
        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M%S")
        self.temp_dir=self.bundle_dir+os.sep+'temp'+os.sep+date_time
        os.mkdir(self.temp_dir)

    def load_annotation(self):
        with open(self.annotation_path) as f:
            self.annoation=json.load(f)

    def split_dataset(self):
        val_num=200 if len(self.annoation)>1000 else int(len(self.annoation)*0.2)+1
        keys=list(self.annoation.keys())
        random.shuffle(keys)
        self.dataset['val']=keys[:val_num]
        self.dataset['train']=keys[val_num:]
        for subset in ['train','val']:
            os.mkdir(self.temp_dir+os.sep+subset)
            self.prepare_data(subset)
            self.prepare_annotation(subset)

    def prepare_data(self,subset):
        for key in self.dataset[subset]:
            file_name=self.annoation[key]['filename']
            shutil.copyfile(self.img_dir+os.sep+file_name,self.temp_dir+os.sep+subset+os.sep+file_name)

    def prepare_annotation(self,subset):
        annotation={i:self.annoation[i] for i in self.dataset[subset]}
        with open(self.temp_dir+os.sep+subset+os.sep+'via_region_data.json', 'w') as outfile:
            json.dump(annotation, outfile)

    def make_zip_file(self):
        shutil.make_archive(self.destination_dir+os.sep+'dataset', 'zip', self.temp_dir)
        shutil.rmtree(self.temp_dir)

    def run(self):
        self.make_temp_dir()
        self.load_annotation()
        self.split_dataset()
        self.make_zip_file()


class Test(object):
    """docstring for Test."""

    def __init__(self):
        super(Test, self).__init__()
        bundle_dir=get_parent_path(4)
        dataset=Dataset()
        dataset.img_dir=bundle_dir+os.sep+'datasets/dog'
        dataset.destination_dir=bundle_dir+os.sep+'temp'
        dataset.annotation_path=bundle_dir+os.sep+'datasets/dog/via_region_data.json'
        dataset.run()

if __name__ == '__main__':
    Test()
