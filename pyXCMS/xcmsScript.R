library(xcms)
#Choose directory...
#myDir = choose.dir()
#setwd(myDir)
stepVal = 0.01
mzDiffVal = 0.01
SNR = 5
myDirs = c("E:/Fraga/Core-DC-07_mzXML/Blanks",
"E:/Fraga/Core-DC-07_mzXML/C18/A_C18",
"E:/Fraga/Core-DC-07_mzXML/C18/B_C18",
"E:/Fraga/Core-DC-07_mzXML/Dil/A_Dil",
"E:/Fraga/Core-DC-07_mzXML/Dil/B_Dil",
"E:/Fraga/Core-DC-07_mzXML/Ext/A_Ext",
"E:/Fraga/Core-DC-07_mzXML/Ext/B_Ext",
"E:/Fraga/Core-DC-07_mzXML/WCX/A_WCX",
"E:/Fraga/Core-DC-07_mzXML/WCX/B_WCX",
"E:/Fraga/Core-DC-07_mzXML/Standards"
)

multEIC <- function(xs, eicwidth = 100, value = c("into","maxo","intb")){
     classeic = levels(sampclass(xs))
     value <- match.arg(value)
     groupmat <- groups(xs)
     if (length(groupmat) == 0)
         stop("No group information found")
     tsidx <- groupnames(xs)
     classlabel <- sampclass(xs)
     classlabel <- levels(classlabel)[as.vector(unclass(classlabel))]
     ceic <- which(classlabel %in% classeic)
     eicmax <- length(groupnames(xs))
     eics <- getEIC(xs, rtrange = eicwidth*1.1,sampleidx = ceic,groupidx = tsidx[seq(length = eicmax)],rt = "corrected")
     eicdir <- paste("EIC", sep="")
     dir.create(eicdir)
     png(file.path(eicdir, "%03d.png"), width = 800, height = 600)
     plot(eics, rtrange = eicwidth, col=array(1:length(sampnames(xs))),legtext=sampnames(xs))
     dev.off()
     }
	 
peakTable <- function(xs){
  if (nrow(xs@groups) > 0) {
     groupmat <- groups(xs)
     ts <- data.frame(cbind(groupmat,groupval(xs, "medret", "into")),row.names = NULL)
     cnames <- colnames(ts)
     colnames(ts) <- cnames
  } else if (length(xs@sampnames) == 1)
        ts <- xs@peaks
    else stop ('First argument must be a xcmsSet with group information or contain only one sample.')
 ts
} 

runXCMS <- function(dirList){
	for(item in dirList){
		setwd(item)
		set=xcmsSet(step=stepVal,mzdiff=mzDiffVal, snthresh = SNR)#mzdiff minimum difference for m/z peaks to be groups in the RT
		set@peaks <- set@peaks[set@peaks[,"mz"] < 350, ]
		#
		xg <- group(set,bw=30,mzwid=0.01,minfrac=0.01, max = 3)
		#could also use the following:
		#xg <- group(set,bw=30)
		xg1=retcor(xg,missing=2, extra=2, method="loess",span=.5, f="symmetric",plottype="mdevden")
		xg2 <- group(xg1, bw=30)
		xg3 <-fillPeaks(xg2)
			 
		multEIC(xg3, eicwidth = 150) 

		#xsetEIC <- getEIC(set, cbind(mzmin=99, mzmax=102))#can use rt = "corrected"
		#plot(xsetEIC, col = c(length(sampnames(set))))

		pt = peakTable(xg3)
		ptName = getwd()[1]
		ptName = paste(ptName, 'csv', sep = '.')
		ptName = basename(ptName)
		write.table(pt,file = ptName, sep = ",", row.names = F)
	}
}
	 

runXCMS(myDirs)

