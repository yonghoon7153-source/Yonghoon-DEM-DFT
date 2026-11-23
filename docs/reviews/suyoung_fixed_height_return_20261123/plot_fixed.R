args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2)
d <- read.csv(args[1], check.names = FALSE)
required <- c("hold_F24_step", "time_since_stop", "F12_floor_MPa", "F24_floor_MPa",
              "floor_gap_MPa", "F12_KE", "F24_KE")
stopifnot(all(required %in% names(d)), nrow(d) == 2401,
          all(d$hold_F24_step == 0:2400), all(diff(d$time_since_stop) > 0),
          all(is.finite(as.matrix(d[required]))),
          max(abs(d$F12_floor_MPa-d$F24_floor_MPa-d$floor_gap_MPa)) < 1e-12)
t <- d$time_since_stop
marks <- t[1 + c(0,600,1200,1800,2400)]
ink <- "#203843"
teal <- "#16776d"
orange <- "#b55430"
axes <- "#81919a"
grid <- "#dae3e6"
band <- c("#f0f5f8","#e5edf2")
reference <- .6636991102836952
png(args[2],width=2200,height=1660,res=160,pointsize=17)
layout(matrix(1:3,3,1), heights=c(1.25,.93,1.05))
par(family="sans",bty="n",las=1,xaxs="i",yaxs="i",lend="round",tcl=-.24,
    mgp=c(2.9,.55,0),cex.axis=1.05,col=ink,col.axis=ink,oma=c(.3,.15,.6,.6))
plot_panel <- function(v, desc, panel, bottom=FALSE) {
  lim <- range(v)
  pad <- max(diff(lim)*.10,1e-9)
  lim <- c(if (min(lim)>=0) max(0,min(lim)-pad) else min(lim)-pad, max(lim)+pad)
  plot.new()
  plot.window(range(t),lim)
  rect(marks[3],lim[1],marks[4],lim[2],col=band[1],border=NA)
  rect(marks[4],lim[1],marks[5],lim[2],col=band[2],border=NA)
  yt <- pretty(lim,n=4)
  yt <- yt[yt>=lim[1] & yt<=lim[2]]
  abline(h=yt,col=grid,lwd=.7)
  axis(2,at=yt,col=axes)
  axis(1,at=marks,labels=if (bottom) sprintf("%.3f",marks) else FALSE,col=axes)
  mtext(paste0(panel,"   ",desc),3,adj=0,line=.34,cex=.96,font=2)
}
draw_pair <- function(a,b) {
  lines(t,a,col=teal,lwd=2.6)
  lines(t,b,col=orange,lwd=2.6,lty=2)
}
par(mar=c(.85,4.35,4.3,1.0))
plot_panel(c(d$F12_floor_MPa,d$F24_floor_MPa),"Bottom pressure (MPa)","A")
draw_pair(d$F12_floor_MPa,d$F24_floor_MPa)
mtext("Bottom pressure after the upper plate stops",3,line=2.87,adj=0,cex=1.32,font=2)
mtext("Quarter-speed compression to 0.12244 particle diameters, then fixed height",
      3,line=1.52,adj=0,cex=.88,col="#49616c")
legend("topright",c("12 cells","24 cells"),col=c(teal,orange),lty=c(1,2),
       lwd=2.6,ncol=2,bty="n",xpd=NA,inset=c(0,-.18),cex=1.04)
par(mar=c(.85,4.35,2.05,1.0))
plot_panel(c(d$floor_gap_MPa,-.05*reference,.05*reference),"Bottom pressure difference: 12 minus 24 cells (MPa)","B")
abline(h=0,col=axes,lwd=.9)
abline(h=c(-.05,.05)*reference,col="#a58954",lty=3,lwd=1.35)
lines(t,d$floor_gap_MPa,col=ink,lwd=2.4)
par(mar=c(4.05,4.35,2.05,1.0))
plot_panel(1e6*c(d$F12_KE,d$F24_KE),"Particle kinetic energy (millionths of a model energy unit)","C",TRUE)
draw_pair(1e6*d$F12_KE,1e6*d$F24_KE)
mtext("Time since plate stopped (model time units)",1,line=1.97,cex=1.02)
mtext("Shading marks the last two observation windows. Dotted lines in B mark 5% of the compression reference.",
      1,line=3.15,adj=0,cex=.78,col="#506775")
invisible(dev.off())
