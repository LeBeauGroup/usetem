import numpy

xy_minx=5120
xy_maxx=60415
xy_miny=5120
xy_maxy=60415

expt=0.001
framet=0
num_fr=1

rangex = xy_maxx - xy_minx
rangey = xy_maxy - xy_miny

num_cps = 1
exposeOverhead = 2
hw_overhead = 0

class TakeBKG():

    def takebkg(self, filename, save_path, numimages):
        self.dismiss()
        numimages = int(numimages)
        filename = filename.strip().replace(' ', '_')
        if filename == '':
            print('No filename given')
        elif numimages < 1:
            print('Number of images must be at least 1')
        else:
            filename = save_path + filename
            # if padgui.Busy:
            #     print('PAD is busy')
            #     return
            try:
                Send_to_Cam('videomodeoff \n')

                Send_to_Cam('padcom milbacksub 0 \n')

                Send_to_Cam(('Set_Take_n %.8f %.8f %d\n' % (expt, framet, numimages)))

                Send_to_Cam(('SetAvgExp %s %d \n' % (filename, numimages)))

                Send_to_Cam(('Exposure %s\n' % filename), False)
                #Checking for recv later
                timeout = num_cps*numimages*max(expt+0.00086,framet) + exposeOverhead+hw_overhead
                print(timeout)
                #Round timeout up to nearest half second
                timeout = timeout*10
                if timeout % 5 != 0:
                    timeout = 5*(timeout//5) + 5
                timeout = timeout/10
                print(timeout)
                padgui.Busy = True
                Clock.schedule_once(padgui.Timeout, timeout)
                Clock.schedule_once(lambda x: self.setbackground(filename), timeout)
            except Exception as e:
                print(e)
