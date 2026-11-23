args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) stop("Expected settings TSV and output PNG")
settings <- read.delim(args[1], check.names = FALSE, na.strings = "",
                       stringsAsFactors = FALSE)
measured <- settings[settings$u6a %in% c("PASS", "FAIL"), ]
cells <- c(8, 12, 16, 24)
phi <- as.matrix(measured[paste0("phi_m_", cells)])
limit <- 0.005
delta <- measured$abs_delta_12_16
stopifnot(identical(measured$setting, 1:2), all(is.finite(phi)),
          all(abs(abs(phi[, 2] - phi[, 3]) - delta) < 1e-12),
          all((delta <= limit) == (measured$u6a == "PASS")))

ink <- "#172B38"
slate <- "#465B66"
colors <- c("#B24E22", "#006C7D")
grid <- "#DBE2E4"
png(args[2], width = 2640, height = 1485, res = 165, pointsize = 20,
    bg = "white")
layout(matrix(1:2, nrow = 1), widths = c(1.65, 1))
par(omi = c(.60, .23, 1.30, .30), family = "sans", fg = ink,
    col.axis = slate, col.lab = ink, xaxs = "i", yaxs = "i",
    tcl = -.17, mgp = c(2.83, .80, 0), lend = "round")

par(mai = c(1.38, 1.24, .56, .33))
plot.new()
plot.window(xlim = c(7, 25), ylim = c(.936, 1.011))
ticks <- c(.94, .96, .98, 1)
abline(h = ticks, col = grid, lwd = 1)
axis(1, at = cells)
axis(2, at = ticks, labels = sprintf("%.2f", ticks), las = 1)
mtext("Grid cells per particle diameter", 1, line = 2.30)
mtext(expression(paste("Reference-area fraction, ", italic(Phi)[m])),
      2, line = 2.95)
mtext("At 1.2 MPa bottom-plate pressure", 3, line = .66,
      cex = 1.02, font = 2, adj = 0, col = ink)
for (row in seq_len(nrow(measured))) {
  lines(cells, phi[row, ], col = colors[row], lwd = 2.65,
        lty = c(2, 1)[row])
  points(cells, phi[row, ], bg = colors[row], col = "white", lwd = 1.6,
         cex = 1.29, pch = c(22, 21)[row])
}
legend("bottomright", c("1   Both controls off", "2   Gap correction only"),
       col = colors, pt.bg = colors, pch = c(22, 21), lwd = 2.25,
       lty = c(2, 1), inset = c(.008, .035), bty = "n", cex = .82,
       text.col = ink, y.intersp = 1.26)

par(mai = c(1.38, .39, .56, .30))
plot.new()
plot.window(xlim = c(0, .0065), ylim = c(0, 2.2))
mtext("12 vs 16 cells", 3, line = .66, font = 2, adj = 0, col = ink)
rect(0, 0, limit, 1.80, col = "#F0F6F5", border = NA)
segments(limit, 0, limit, 1.78, col = slate, lty = 2, lwd = 1.6)
text(limit, 1.95, "0.005 limit", adj = c(.84, .5), cex = .82, col = slate)
axis(1, at = c(0, .002, .004, .006),
     labels = c("0", "0.002", "0.004", "0.006"), cex.axis = .86)
mtext(expression(paste("Absolute difference in ", italic(Phi)[m])),
      1, line = 2.30)
for (row in seq_len(nrow(measured))) {
  y <- c(1.22, .47)[row]
  segments(0, y, delta[row], y, lwd = 2, col = colors[row])
  points(delta[row], y, pch = c(22, 21)[row], bg = colors[row],
         col = "white", cex = 1.3, lwd = 1.6)
  label <- sprintf("Setting %d   %.6f   %s", measured$setting[row],
                   delta[row], measured$u6a[row])
  text(.00008, y + .24, label, adj = 0, col = colors[row], cex = .85,
       font = 2)
}

mtext("Gap correction meets the registered 0.005 limit", 3, outer = TRUE,
      line = 1.52, adj = .045, font = 2, col = ink, cex = 1.43)
mtext("The first passing setting is retained for U6(b) and U6(c).",
      3, outer = TRUE, line = .29, adj = .06, col = slate, cex = .88)
mtext("Development data   |   23 Nov 2026   |   One loading trace per grid and setting.",
      1, outer = TRUE, line = .15, adj = .045, cex = .74, col = slate)
invisible(dev.off())
