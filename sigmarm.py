'''
Plotting the expected depolarisation according to the External Faraday Dispersion model (e.g. Sokoloff et al. 1998)
This is equivalent to the 'm2' model of RM-Tools QU-fitting

y-axis is the amount of depolarisation (p/p_0), with p_0 being the intrinsic fractional polarisation. No depolarisation = 1; Complete depolarisation = 0

x-axis shows frequency as the ticks, but is in fact linear to lambda^2 [m^2]
'''

import numpy as np
import matplotlib.pyplot as plt



'''
Change settings below
'''

## Plotting [low_freq, high_freq] in Hz; supports np.infty
#freq_range = [565.e6, np.infty] ## Better suited for MeerKAT
freq_range = [299.e6, np.infty] ## Better suited for SKA

obs_setup_list = {
## Dictionary of observational setup to be plotted
## Comment out ones to be skipped
## Add new ones if applicable
## 
## <setup_name>: [<freq_low_hz>, <freq_high_hz>, <plot_alpha>, <plot_color>],
#'MMGPS-UHF': [580.e6, 1015.e6, 0.2, 'r'],
#'MMGPS-L': [900.e6, 1670.e6, 0.2, 'g'],
#'MMGPS-S': [1968.e6, 2843.e6, 0.2, 'b'],
'SKA-Low': [50.e6, 350.e6, 0.2, 'k'],
'SKA-Mid Band 1': [350.e6, 1050.e6, 0.2, 'r'],
'SKA-Mid Band 2': [950.e6, 1760.e6, 0.2, 'g'],
'SKA-Mid Band 3': [1650.e6, 3050.e6, 0.2, 'y'],
'SKA-Mid Band 4': [2800.e6, 5180.e6, 0.2, 'c'],
'SKA-Mid Band 5a': [4600.e6, 8500.e6, 0.2, 'b'],
'SKA-Mid Band 5b': [8300.e6, 15400.e6, 0.2, 'm'],
}

## sigma_RM plotted in radm-2
#sigma_rm_list = [0, 5, 10, 30] ## Better suited for MeerKAT
sigma_rm_list = [0, 1, 5, 20] ## Better suited for SKA
style_list = ['k-', 'r-', 'b-', 'm-'] ## Plotting style matching sigma_rm_list

plt.figure(figsize=(10., 4.)) ## Change the figure size here

## Frequencies to draw x-ticks; in MHz; supports np.infty
#plt_x_ticks_list = [580, 800, 1000, 2000, np.infty] ## Better for MeerKAT
plt_x_ticks_list = [300, 350, 500, 800, 1400, np.infty] ## Better for SKA

## Output figure file name; set to None to show plot directly
#output_file_name = 'sigma_rm.png'
output_file_name = None

'''
Change settings above
'''

c = 299792458. ## Speed of light
l2 = np.arange((c/freq_range[1])**2, (c/freq_range[0])**2, ((c/freq_range[0])**2-(c/freq_range[1])**2)/1000.) ## Lambda2 values to be plotted; divide into 1000 steps



## Plotting the frequency ranges of the observation setup
for obs_setup in obs_setup_list:
   low_l2 = (c/obs_setup_list[obs_setup][1])**2
   high_l2 = (c/obs_setup_list[obs_setup][0])**2
   plt_alpha = obs_setup_list[obs_setup][2]
   plt_color = obs_setup_list[obs_setup][3]
   plt.axvspan(low_l2, high_l2, alpha=plt_alpha, color=plt_color)

## Plotting the sigma_RM across frequency
for i in range(len(sigma_rm_list)):
   sigma_rm = sigma_rm_list[i]
   plot_style = style_list[i]
   plt.plot(l2, np.exp(-2.*sigma_rm**2*l2**2), plot_style, label=r'$\sigma_{\rm RM} = '+str(sigma_rm)+r'\,{\rm rad\,m}^{-2}$')

## Wrapping up the figure
plt_x_ticks_string = []
plt_x_ticks_float = []
for plt_x_ticks in plt_x_ticks_list:
   if plt_x_ticks == np.infty:
      plt_x_ticks_string.append(r'$\infty$')
      plt_x_ticks_float.append(0)
   else:
      plt_x_ticks_string.append(str(plt_x_ticks))
      plt_x_ticks_float.append((c/(plt_x_ticks*1.e6))**2)

plt.xticks(plt_x_ticks_float, plt_x_ticks_string, fontsize=16)
plt.xlim(np.min(l2), np.max(l2))
plt.yticks(fontsize=16)
plt.xlabel('Frequency (MHz)', fontsize=16)
plt.ylabel(r'$p/p_0$', fontsize=16)
plt.legend(loc='upper right', fontsize=14)
plt.tight_layout()
if output_file_name == None:
   plt.show()
else:
   plt.savefig(output_file_name)










