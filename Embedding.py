from flask import Flask
from stock_phase1 import plot_figure

app=Flask(__name__)
app.config["DEBUG"]=True
@app.route('/stock_phase1')
def plot_figure():
	plt.figure(figsize = (18,9))
	plt.plot(range(df.shape[0]),all_mid_data,color='b',label='True')
	plt.plot(range(0,N),run_avg_predictions,color='orange', label='Prediction')
	#plt.xticks(range(0,df.shape[0],50),df['Date'].loc[::50],rotation=45)
	plt.xlabel('Date')
	plt.ylabel('Mid Price')
	plt.legend(fontsize=18)
	plt.show()
	  

