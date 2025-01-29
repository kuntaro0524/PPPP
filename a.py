from scipy import stats

x=[5.05,6.75,3.21,2.66]
y=[1.65,26.5,-5.93,7.96]

gradient,intercept,r_value,p_value,std_err=stats.linregress(x,y)
print "Gradient and intecept", gradient, intercept

print "R-squared", r_value**2
print "p-value",p_value


print "UNKO"
