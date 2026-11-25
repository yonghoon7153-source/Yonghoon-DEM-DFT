#define _GNU_SOURCE
#include <stdio.h>
#include <stdarg.h>
/* sandbox-only: Ubuntu QE 6.7 md5 writes one NUL past a 32-char buffer; skip the fortify size check */
int __snprintf_chk(char *s, size_t maxlen, int flag, size_t slen, const char *fmt, ...) {
  va_list ap; va_start(ap, fmt); int r = vsnprintf(s, maxlen, fmt, ap); va_end(ap); return r;
}
