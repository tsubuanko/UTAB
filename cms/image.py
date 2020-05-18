import os
import config.settings
def get_image_path(self,filename):
    prefix='media/profile_picture'
    name=str(uuid.uuid4()).replace('-','')
    extension=os.path.splitext(filename)[-1]
    return prefix+name+extension
def delete_previous_file(function):
    def wrapper(*args,**kwargs):
        self=args[0]
        result=Image.objects.filter(pk=self.pk)
        previous=result[0] if len(result) else None
        super(Image,self).save()
        result=function(*args,**kwargs)
        if previous:
            os.remove(MEDIA_ROOT+'/')
        return wrapper
