'''
Plotting the expected polarised source count against sigma_RM values

Predictions following Rudnick & Owen (2014); sigma_RM from External Faraday Dispersion (e.g. Sokoloff et al. 1998), which is equivalent to the 'm2' model of RM-Tools QU-fitting

Required user inputs:
- Frequency coverage of the instrument
- 1-sigma RMS noise level
'''

import numpy as np
import matplotlib.pyplot as plt



'''
Change settings below
'''

## Range of sigma_RM to try
#sigmaRM_list = np.arange(0., 50.01, 0.01) ## Better suited for MeerKAT
sigmaRM_list = np.arange(0., 100.1, 0.1) ## Better suited for SKA

survey_library = {
## <Survey Name>: [rms_1sigma_uJy/beam, freq_low_hz, freq_high_hz, plot_colour],
#'POSSUM Expected': [18., 800.e6, 1088.e6, 'k'],
#'MMGPS-L Expected': [14., 900.e6, 1670.e6, 'r'],
#'MMGPS-S Expected': [9., 1968.e6, 2843.e6, 'b'],
'SKA-Mid Band 1': [2.34, 350.e6, 1050.e6, 'r'], ## SKA-Mid AA4 Band 1 1 hr; robust=0; no tapering
'SKA-Mid Band 2': [1.14, 950.e6, 1760.e6, 'g'], ## SKA-Mid AA4 Band 2 1 hr; robust=0; no tapering
'SKA-Mid Band 5a': [0.70, 4600.e6, 8500.e6, 'b'], ## SKA-Mid AA4 Band 5a 1 hr; robust=0; no tapering
'SKA-Mid Band 5b': [0.84, 8300.e6, 15400.e6, 'm'], ## SKA-Mid AA4 Band 5b 1 hr; robust=0; no tapering
## 
## Above are the "default" with SKA AA4
## Special cases (mainly SKA AA*) below
## 
#'SKA-Mid Band 2': [11.4, 950.e6, 1760.e6, 'g'], ## SKA-Mid AA* Band 2 wide (6.4 min; robust = -1)
#'SKA-Mid Band 2': [1.31, 950.e6, 1760.e6, 'g'], ## SKA-Mid AA* Band 2 deep (8 hr; robust = -1)
#'SKA-Mid Band 2 ultra-deep': [0.03715, 950.e6, 1760.e6, 'g'], ## SKA-Mid AA* Band 2 ultra-deep HI commensal (10,000 hr; robust = -1)
#'SKA-Mid Band 3': [0.9, 1650.e6, 3050.e6, 'y'], ## SKA-Mid AA* Band 3 test
#'SKA-Mid Band 5a': [3.7, 4600.e6, 8500.e6, 'b'], ## SKA-Mid AA* Band 5a; 10 min
#'SKA-Mid Band 5a': [2.56, 4600.e6, 8500.e6, 'b'], ## SKA-Mid AA* Band 5a; 15 min, 0.2" tapering
}

plt.figure(figsize=(10., 4.))
xscale = 'log' ## x-axis plotting in 'linear' or 'log' scale

'''
Change settings above
'''



def get_srccount(noise, freq, sigmaRM_range):
   ## Noise is 1-sigma (uJy/beam)
   ## Freq is the observing frequency (Hz)
   ## sigmaRM_range is a list of sigmaRM to try (radm-2)
   sncut = 6. ## S/N cut in polarisation
   spix = -0.7 ## Spectral index
   ## Extrapolate from observed frequency to 1.4 GHz equivalent
   p_Lband = sncut*noise*(1.4e9/freq)**spix
   ## Apply the depolarisation factor
   p_Lband = p_Lband/np.exp(-2.*sigmaRM_range**2*(299792458./freq)**4)
   ## Calculate the source density
   nsrc = 45.*(p_Lband/30)**-0.6
   return nsrc



max_srccount = 0 ## Store the maximum value to set ylim

for survey in survey_library:
   srccount_list_low = get_srccount(survey_library[survey][0], survey_library[survey][1], sigmaRM_list)
   srccount_list_high = get_srccount(survey_library[survey][0], survey_library[survey][2], sigmaRM_list)
   plt.fill_between(sigmaRM_list, srccount_list_low, srccount_list_high, color=survey_library[survey][3], alpha=0.2, label=survey)
   max_srccount = np.max([max_srccount, np.max(srccount_list_low)])
   max_srccount = np.max([max_srccount, np.max(srccount_list_high)])



## Wrap up the figure
plt.xscale(xscale)
plt.xlim(np.min(sigmaRM_list), np.max(sigmaRM_list))
plt.ylim(0., max_srccount*1.1)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel(r'$\sigma_{\rm RM}$'+' (rad m'+r'$^{-2}$'+')', fontsize=16)
plt.ylabel('Pol. Source Density (deg'+r'$^{-2}$'+')', fontsize=16)
plt.legend(loc='upper right', fontsize=14)
plt.tight_layout()
plt.show()








