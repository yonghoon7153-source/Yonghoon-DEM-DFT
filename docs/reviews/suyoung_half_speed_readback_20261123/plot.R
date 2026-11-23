args <- commandArgs(trailingOnly=TRUE)
d <- read.csv(args[1], na.strings="", check.names=FALSE)
ref <- as.numeric(args[3])
dk <- d[!is.na(d$original_F24_step),]
png(args[2], width=1800, height=1180, res=172)
par(family="sans", fg="#223543", col.axis="#324956", col.lab="#223543",
    xaxs="i", yaxs="i", bty="n", las=1, tcl=-0.24, lend="round")
original <- "#16658A"
half <- "#BD502D"
rule <- "#CBD4DA"
boundary <- "#728768"
band <- "#EAF0E7"
txt <- "#1F3441"
xlim <- c(0,.176)
xat <- seq(0,.175,.025)
layout(matrix(1:2,ncol=1),heights=c(1.19,1))

axes <- function(yr, yname, xlabel, bgband=FALSE) {
  plot.new(); plot.window(xlim,yr)
  if(bgband)
    rect(xlim[1],-ref*.05,xlim[2],ref*.05,col=band,border=NA)
  at <- pretty(yr,n=5)
  at <- at[at>=yr[1] & at<=yr[2]]
  abline(h=at, col=rule,lwd=.6)
  axis(1,at=xat,labels=if (xlabel) sprintf("%.3f",xat) else FALSE,
       col="#758995",col.ticks="#758995",cex.axis=.91)
  axis(2,at=at,labels=sprintf("%.2f",at),col="#758995",col.ticks="#758995",cex.axis=.91)
  mtext(yname,3,line=.55,adj=0,col=txt,cex=.99,font=2)
}

par(mar=c(2.0,4.8,5.5,1.15))
both <- c(dk$original_delta_MPa,d$half_delta_MPa)
range_gap <- range(c(-ref*.05,ref*.05,both))
dy <- diff(range_gap)
axes(range_gap+c(-.12,.23)*dy,"Bottom plate pressure difference: F12 minus F24 (MPa)",FALSE,TRUE)
mtext("Grid sensitivity at two plate speeds",3,line=3.72,adj=0,font=2,col=txt,cex=1.76)
mtext("Early compression with the same material-point lid",3,line=2.10,adj=0,col="#526977",cex=1.02)
abline(h=c(-1,1)*ref*.05,col=boundary,lwd=.9,lty=3)
lines(dk$plate_travel_D, dk$original_delta_MPa,col=original,lwd=2.15)
lines(d$plate_travel_D, d$half_delta_MPa,col=half,lwd=2.15)
mark <- function(frame, values, color) {
  idx <- which.max(abs(values))
  points(frame$plate_travel_D[idx],values[idx],pch=21,col="white",bg=color,lwd=1.2,cex=1.27)
}
mark(dk,dk$original_delta_MPa,original)
mark(d,d$half_delta_MPa,half)
legend("topleft",legend=c("Original speed","Half speed","5% band (+/-0.03318 MPa)","Peak absolute gap"),
       col=c(original,half,boundary,"#566572"),lwd=c(2.2,2.2,1,NA),lty=c(1,1,3,NA),
       pch=c(NA,NA,NA,16),bty="n",cex=.88,ncol=1,y.intersp=.99,inset=c(.005,.005))

par(mar=c(4.15,4.8,2.15,1.15))
max_p <- max(d[c("original_F12_MPa","original_F24_MPa","half_F12_MPa","half_F24_MPa")],na.rm=TRUE)
axes(c(0,1.13*max_p),"Bottom plate pressure (MPa)",TRUE)
lines(dk$plate_travel_D,dk$original_F12_MPa,col=original,lwd=1.95,lty=1)
lines(dk$plate_travel_D,dk$original_F24_MPa,col=original,lwd=1.95,lty=2)
lines(d$plate_travel_D,d$half_F12_MPa,col=half,lwd=1.95,lty=1)
lines(d$plate_travel_D,d$half_F24_MPa,col=half,lwd=1.95,lty=2)
legend("topleft", legend=c("Original: F12","Original: F24","Half: F12","Half: F24"),
       col=c(original,original,half,half),lty=c(1,2,1,2),lwd=1.9,bty="n",cex=.88,ncol=2,y.intersp=1.05)
mtext("Plate travel / particle diameter",1,line=2.55,cex=1.04,col=txt)
invisible(dev.off())
