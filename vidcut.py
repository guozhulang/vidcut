# -*- coding: utf-8 -*-
import subprocess, re, os
from datetime import date, time, datetime


class VidCutter:
    def __init__(self, invid):
        self.input_video = invid
        self.duration = self.__getDuration()
        self._date = date(1,1,1)

    def __getDuration(self):
        ffmpeg = subprocess.Popen(['ffmpeg', '-i', self.input_video], stderr=subprocess.STDOUT, stdout=subprocess.PIPE )
        out, err = ffmpeg.communicate()
        duration = re.findall('Duration: ([0-9]{2}:[0-9]{2}:[0-9]{2})', out)
        if len(duration) == 0:
            return '0'
        else:
            return duration[0]


    def timediff(self, stime, etime):
        stime = stime.split(":")
        stime = time(int(stime[0]), int(stime[1]), int(stime[2]))
        etime = etime.split(":")
        etime = time(int(etime[0]), int(etime[1]), int(etime[2]))   
        tdiff = datetime.combine(self._date, etime) - datetime.combine(self._date, stime)
        return str(tdiff)
        

    def get_left_part(self, ctime, reverse_time=False):
        #checking ctime complement
        ctime_comp = self.timediff(ctime, self.duration)
        if ctime_comp[0]=='-': #if it's negative
            raise ValueError("Invalid cutting time")         
        
        if reverse_time:
            #cutting time is measured from the right side
            length = ctime_comp
        else:
            length = ctime
            
        outvid = self.input_video[:-4] + "_left" + self.input_video[-4:]
        ffmpeg = subprocess.Popen(["ffmpeg", "-i", self.input_video,
                                   "-acodec", "copy", "-vcodec", "copy",
                                   "-ss", "0", "-t", length, outvid],
                                   stderr=subprocess.STDOUT, stdout=subprocess.PIPE)        
        out, err = ffmpeg.communicate()
        

    def get_right_part(self, ctime, reverse_time=False):
        #checking ctime complement
        ctime_comp = self.timediff(ctime, self.duration)
        if ctime_comp[0]=='-': #if it's negative
            raise ValueError("Invalid cutting time")
                       
        if reverse_time:
            #cutting time is measured from the right side
            length = ctime
            ctime = ctime_comp
        else:
            length = ctime_comp                        
          
        outvid = self.input_video[:-4] + "_right" + self.input_video[-4:]
        ffmpeg = subprocess.Popen(["ffmpeg", "-i", self.input_video,
                                   "-acodec", "copy", "-vcodec", "copy",
                                   "-ss", ctime, "-t", length, outvid],
                                   stderr=subprocess.STDOUT, stdout=subprocess.PIPE)        
        out, err = ffmpeg.communicate()        
        

    def get_cut_parts(self, ctime, reverse_time=False):
        self.get_left_part(ctime, reverse_time)
        self.get_right_part(ctime, reverse_time)
        


if __name__ == '__main__':
    import sys, os
    import os.path
       
    if len(sys.argv) < 3:
        sys.exit()
        
    ## parameters passed are
    #1. filename or folder of a collection of files        
    #2. cutting time
    #3. (optional) both, left, right (output pieces) default is `both`   
    #4. (optional) rev : time given is reversed (from right to left)
        
    piece = "both"
    rev_time = False
    
    ########################################################################## 
    
    def cut(vfile, ctime, piece, rev_time):
        try:
            vc = VidCutter(vfile)
            print "Processing:", '"'+ vfile +'"',
            if piece == 'left':
                vc.get_left_part(ctime, rev_time)
            elif piece == 'right':
                vc.get_right_part(ctime, rev_time)
            else:
                vc.get_cut_parts(ctime, rev_time)
        except ValueError:
            print ">> The Cutting time is not valid for this file",
        except:
            print ">> Error processing the file",
            
        print "" #end the message line
        
    ##########################################################################    

    if len(sys.argv) > 3 and sys.argv[3] in ['left', 'right']:
        piece = sys.argv[3]
        
    if len(sys.argv) > 4 and sys.argv[4] == 'rev':
        rev_time = True
    
    if os.path.isdir(sys.argv[1]):
        for parent, dirs, files in os.walk(sys.argv[1]):
            for f in files:
                if f[-4:] in ['.mp4', '.avi', '.wmv', '.mpg', '.mov', '.flv']:
                    cut(os.path.join(parent, f), sys.argv[2], piece, rev_time)
    elif os.path.isfile(sys.argv[1]):
        cut(sys.argv[1], sys.argv[2], piece, rev_time)
    else:
        sys.exit("Invalid input")
        
    print "Done!"

                    