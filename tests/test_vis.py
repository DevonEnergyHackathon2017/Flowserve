from well_vis_class import well_vis
import plotly

def main():
	print('Testing vis')
	wv_obj = well_vis(3)
	fig = wv_obj.do_plot()
	plotly.offline.plot(fig, filename = 'well_model.html')

if __name__ == '__main__':
	main()