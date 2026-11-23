args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2)
d <- read.csv(args[1], check.names = FALSE)
stopifnot(nrow(d) == 1139, all(diff(d$displacement_D) > 0))
v <- d$displacement_D
reference <- 0.6636991102836952
palette <- c("#394e68", "#b35630", "#127970")
ink <- "#1b3440"
axis_col <- "#8799a2"
grid_col <- "#e0e7e8"
png(args[2], width = 1920, height = 1320, res = 175, pointsize = 15)
par(family = "sans", las = 1, bty = "n", lend = "round", xaxs = "i", yaxs = "i", col = ink,
    col.axis = ink, tcl = -0.23, mgp = c(2.2,.48,0), cex.axis = .90)
layout(matrix(c(1,2), nrow=2), heights=c(1,1.14))
axes <- function(yt, fmt, bottom=TRUE) {
  axis(1, at=seq(0,.16,.02), labels=if (bottom) sprintf("%.2f",seq(0,.16,.02)) else FALSE, col=axis_col)
  axis(2, at=yt, labels=sprintf(fmt, yt), col=axis_col)
}
par(mar=c(1.6,4.55,4.3,.95))
plot.new()
plot.window(xlim=c(0,.172),ylim=c(0,.172))
abline(h=seq(0,.16,.04),col=grid_col)
lines(v,d$quarter_F12_MPa,lwd=2.7,col=palette[3])
lines(v,d$quarter_F24_MPa,lwd=2.7,lty=2,col=ink)
axes(seq(0,.16,.04),"%.2f",FALSE)
mtext("Bottom pressure (MPa)",2, line=3.15,las=0,cex=.90)
mtext("Bottom pressure at quarter speed",3,adj=0,line=2.35,cex=1.25,font=2)
mtext("Both grids sampled at the same plate travel",3,adj=0,line=.75,cex=.91,col="#536770")
legend("topleft",c("12 cells","24 cells"),col=c(palette[3],ink),lty=c(1,2),lwd=2.7,
       bty="n",cex=.90,inset=.012)
par(mar=c(3.6,4.55,3.3,.95))
plot.new()
plot.window(xlim=c(0,.172),ylim=c(-6,22))
rect(0,-5,.172,5,col="#e6f1ed",border=NA)
abline(h=c(0,10,15,20),col=grid_col)
abline(h=c(-5,5),col="#71988b",lty=3,lwd=1.1)
tags <- c("original","half","quarter")
for (i in seq_along(tags)) {
  percent <- d[[paste0(tags[i],"_gap_MPa")]]*100/reference
  lines(v,percent,col=palette[i],lwd=2.2,lty=c(3,2,1)[i])
  peak <- which.max(abs(percent))
  points(v[peak],percent[peak],pch=21,bg=palette[i],col="white",lwd=1.1,cex=1)
}
axes(c(-5,0,5,10,15,20),"%.0f")
mtext("Grid difference (%)",2,line=3.15,las=0,cex=.90)
mtext("Plate travel / initial particle diameter",1,line=2.18,cex=.95)
mtext("12-cell minus 24-cell pressure at three plate speeds",3,adj=0,line=1.68,cex=1.10,font=2)
mtext("Shading: within 5% of the reference (0.66370 MPa). Dots mark maximum absolute differences.",3,adj=0,line=.32,cex=.83,col="#536770")
legend("topleft",c("Original speed","Half speed","Quarter speed"), col=palette,lty=c(3,2,1),lwd=2.4,
       bty="n",cex=.85,inset=.009)
invisible(dev.off())
