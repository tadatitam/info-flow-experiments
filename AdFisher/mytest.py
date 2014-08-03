import sys
import core.adfisher as adfisher

t = sys.argv[1]
log_file = t

adfisher.run_kw_analysis(log_file, keywords=['dating'], verbose=True)
