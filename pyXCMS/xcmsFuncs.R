writePeakTable <- function(xs, path){
  if (nrow(xs@groups) > 0){
     groupmat <- groups(xs)
     ts <- data.frame(cbind(groupmat,groupval(xs, "medret", "into")),row.names = NULL)
     cnames <- colnames(ts)
     colnames(ts) <- cnames
  }
  else if (length(xs@sampnames) == 1)
        ts <- xs@peaks
  else stop ('First argument must be a xcmsSet with group information or contain only one sample.')
  write.table(ts, file = path, sep = ",", row.names = F)
  ts
}
