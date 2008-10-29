import numpy as N
import pylab as P

def fastpa(f, r, s, r1, r2,  option, fig = True):


    '''
    function [fspek,optima]=fastpa(f,r,s,ra1,ra2,option, fig)

    %    FUNCTION: [fspek,optima]=fastpa(f,r,s,ra1,ra2,option, fig)
    %
    %    Shiftcorrection of a spectra against a reference
    %    spectra, simultaneous sideways movement and interpolation.
    %    evaluation: correlation coefficient
    %
    %    INPUT:    f    -    Spectra to be shift corrected
    %            r    -    Reference spectra
    %                    (f and r must be of the same length)
    %            s    -    number of segments to devide spectra in
    %            ra1    -    max range of sideway movements, [-ra1 ra1]
    %            ra2    -    max range of interpolation, [-ra2 ra2]
    %            option-    if 1, beam width = 1
    %                    else if 2, beam width  = 2
    %            fig -    fig = 1 draws the result
    %
    %    OUTPUT:    spek    -    shift corrected spectra
    %            optima    -    The optimal phasing parameters
    %
    %     by Geun Cheol Lee 2003-12-22 (slightly modified from Jenny Forshed's GA version)
    %
    '''

    #global ff rr

    #take the real part of spectra
    f = N.real(f)
    r = N.real(r)


    # transpose if vectors in wrong direction
#    if size(f,1) > size(f,2)
#       f=f[N.newaxis,:];
#    end
#    if size(r,1) > size(r,2)
#       r=r';
#    end

    #disp(coco(r,f));
    #t0=clock;

    segm = N.floor(len(f)/s)# minimum size of segment
    stop = segm # give end point for the first segment
    start = 1  # give start point for the first segment
    fspek = []
    optima = []
    sta = []
    sto = []
    # find minimum in f(:,stop:(stop+500)) och r(:,stop:(stop+500))
    while stop < len(f) - 500:
        n = 40
        l = 0
        ii = []
        while len(ii) == 0:#isempty(ii) == 1
            ii, indf = findmin(f[stop:stop+500],r[stop:stop+500],n+1)#,stop:(stop+500)), r(:,stop:(stop+500)), n+l);
            l = l + 20
        i = indf[ii[0]] # take the first of the first...
        stop +=i


       #% define the segmentet to be shiftcorrected
        ff = f[start:stop]#(:,start:stop);
        rr = r[start:stop]#r(:,start:stop);

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #% Local search  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%------------------------------------------
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        opti = [0, 0, 0]
        opti = beamsearch(r1, r2, ff, rr, option)
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        #% Optimum values from the GA
        inter = N.round(opti[0]);
        sid = round(opti[1]);

        # interpolation
        if len(ff) > 0 & inter != 0:
            step = (len(ff)+ inter)/(len(rr))
            fff = interp1(ff,N.arange(0,len(ff),step))#[1:step:length(ff)]);
            if len(fff) > len(rr):
                fff = fff[0:len(rr)]#(1:length(rr));
            elif len(fff) <= len(rr):
                diff = len(rr)-len(fff)
                fff = N.append(fff, N.ones(diff)*fff[len(fff)])

        elif len(ff) > 0 and inter == 0:
            fff = ff
        else:
            return

        #% sideways movement
        if len(fff) > 0:
            if sid > 0:
                sidtill = N.ones(sid)*fff[0]
                ffff = N.append(sidtill, fff[0:(len(fff)-sid)])#(1:(length(fff) - sid))];
            elif sid <= 0:
                sid = N.abs(sid)
                sidtill = N.ones(sid)*fff[len(fff)]
                ffff = N.append(fff[(sid+1):len(fff)], sidtill)
        else:
            return

       #% Collect start and end points for plot
        sta.append(start)# = [sta, start];
        sto.append(stop)# = [sto, stop];

       #% Define next start and endpoint
        start = stop + 1
        stop = stop + segm

       #% Collect the shiftcorrected segments
        N.append(fspek,ffff)# = [fspek, ffff]
        N.append(optima,opti)# = [optima, opti]

    #%///////////////////////////////////////////////////////////////////////////
    #% Make fspek size same with r : modified by Lee
    if len(fspek) <= len(r):
        diff = len(r)-len(fspek)
        N.append(fspek, N.ones(diff)*fspek[len(fspek)])
    #%///////////////////////////////////////////////////////////////////////////
    return fspek, optima
    #% Draw-------------------------
#    P.plot(r,'b)
#    P.plot(fspek, 'g')
#    P.plot(sta,f[sta],'.k')
#    P.show()

#    if fig == 1
#        figure
#        hold off
#        plot(real(r),'b');
#        hold on
#        plot(real(f),'r');
#        plot(real(fspek),'g');
#       plot(sta,real(f(sta)),'.k')
#    %   title('target - blue, uncorrected signal - red, corrected signal - green');
#       xlabel('Point Number');
#       ylabel('Intensity Value');
#    end
#    %-------------------------------------------
#
#    finalcc = coco(r,fspek);
#    %disp( [coco(r,fspek) etime(clock, t0)]);
#
#    %format short;
#    %disp(optima);
#    %disp(sta);
#    %disp(sto);
#
#    GL=[]; BL=[];
#    for s=1:length(optima),
#        if coco(r(sta(s):sto(s)),fspek(sta(s):sto(s))) > .5
#             GL = [GL, s];
#        else
#             BL = [BL, s];
#        end
#    end
#    if isempty(GL)
#        disp('Inconsistency: The data could not be aligned because the correlation coefficients for all segments were below the value of the parameter TCC. See the readme.txt file for more information.');
#        return;
#    end
#
#    for i=1:length(BL);
#        a = max(GL(find(GL < BL(i))));
#        b = min(GL(find(GL > BL(i))));
#        if isempty(a), a=b; end
#        if isempty(b), b=a; end
#        new_i = (optima(a, 1)+optima(b, 1))/2;
#        new_s = (optima(a, 2)+optima(b, 2))/2;
#
#        new_i = round(new_i);
#        new_s = round(new_s);
#
#        ff = f(:,sta(BL(i)):sto(BL(i)));
#        rr = r(:,sta(BL(i)):sto(BL(i)));
#
#        if new_i ~= 0
#            step = (length(ff)+ new_i)/(length(rr));
#              fff = interp1(ff,[1:step:length(ff)]);
#              if length(fff) > length(rr)
#                   fff = fff(1:length(rr));
#              elseif length(fff) <= length(rr)
#               diff = length(rr)-length(fff);
#                   fff = [fff ones(1,diff)*fff(length(fff))];
#              end
#        elseif new_i == 0
#            fff = ff;
#        end
#
#        if new_s > 0
#                   sidtill = ones(1,new_s)*fff(1);
#                   ffff = [sidtill fff(1:(length(fff) - new_s))];
#        elseif new_s <= 0
#                   new_s= abs(new_s);
#                  sidtill = ones(1,new_s)*fff(length(fff));
#                   ffff = [fff((new_s+1):length(fff)) sidtill];
#        end
#        fspek(:,sta(BL(i)):sto(BL(i))) = ffff;
#
#        ccc = coco(r(:,sta(BL(i)):sto(BL(i))),fspek(:,sta(BL(i)):sto(BL(i))));
#        if ccc <=1 & ccc >=-1
#            optima(BL(i),:) = [new_i, new_s,  ccc];
#        else
#            optima(BL(i),:) = [new_i, new_s,  0];
#        end
#    end
#
#
#    finalcc = coco(r,fspek);
#    disp( [coco(r,fspek) etime(clock, t0)]);
#
#    %disp(optima);
#
#
#    fid = fopen('estime.txt', 'a');
#    fprintf(fid, '%f ', etime(clock,t0));
#    fclose(fid);
#
#    fid = fopen('output.txt', 'a');
#    fprintf(fid, '%f ', finalcc);
#    fclose(fid);
#
#    %fid = fopen('output2.txt', 'a');
#    %fprintf(fid, '%f ', optima(:,1));
#    %fprintf(fid, '\n');
#    %fprintf(fid, '%f ', optima(:,2));
#    %fprintf(fid, '\n');
#    %fprintf(fid, '%f ', optima(:,3));
#    %fprintf(fid, '\n');
#    %fclose(fid);
#
#    disp('Done !')
#    return


#find minimum in fff and rrr----------------------
def findmin(fff, rrr, n):
    indf = N.argsort(fff)
    #bf,indf] = sort(fff)
    indr = N.argsort(rrr)# [r,indr] = sort(rrr);
    #% Find index equal in f and r
    ii = []
    for k in xrange(n):
        #% see if some of the n lowest points in f equals
        #% some of the n lowest points in r with 40 points of margin
        ij = N.where(indf[0:n] >= indr[k]-20 and indf[0:n] < indr[k]+20)
        if  len(ij) != 0:#isempty(ij) == 0
            ii.append(ij[0])# = [ii ij(1)]; % collect the first matchings

    return ii,indf


if __name__ == "__main__":

    spec = P.load('sample.txt', delimiter = '\t')
    r = spec[:,0]
    s = spec[:,1]
    fspek, optima = fastpa(s, r, 100, 100, 0, option = 2)#, fig = True)
#[fspek,optima]=fastpa(F, R, 100, 100, 0, 2, 1);
    P.plot(fspek, 'g')
    P.plot(r, 'b')
    P.plot(s, 'r')
    P.show()


