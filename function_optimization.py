import time
import xlsxwriter
import numpy as np
import pandas as pd
import SwarmPackagePy as sp
from SwarmPackagePy import testFunctions as tf
from SwarmPackagePy import animation, animation3D

dimensions = [2, 10]
function_names = ['ackley_function', 'sphere_function']
function_calls = [getattr(tf, x) for x in function_names]
optimization_tecs = ['ca', 'ba', 'ssa']
optimization_calls = [getattr(sp, x) for x in optimization_tecs]

iterations = 100
population = 50
rounds = 15

for optimization in optimization_calls:
	for function in function_calls:
		for dimension in dimensions:
			best_agents = []
			time_records = []
			performance_records = []
			best_iterations = []
			for run in range(rounds):
				start = time.time()
				print("Run: #", run, " Dimension: ", dimension, "Function: ", function, "Optimization: ", optimization)
				agents = []
				iteration_records = []
				for iteration in range(iterations):
					print("iteration: #", iteration, end=" ")
					result = optimization(50, function, -10, 10, dimension, 15)
					agents.append(result.get_Gbest())
					iteration_records.append(iteration)

				best_agent = agents[0]
				min = function(best_agent)
				for agent in agents:
					current_value = function(agent)
					if min > current_value:
						min = current_value
						best_agent = agent

				end = time.time()
				elapsed_time = end - start
				performance = function(best_agent)

				best_agents.append(best_agent)
				time_records.append(elapsed_time)
				performance_records.append(performance)
				best_iterations.append(iteration_records[agents.index(best_agent)])
				print('Time Elapsed: ', elapsed_time)
			file_name = optimization.__name__ + "_" + function.__name__ + "_" + str(dimension) + ".xlsx"
			print(file_name)
			df = pd.DataFrame(data={"Time": time_records, "Performance": performance_records, "Agents": best_agents, "Iteration": best_iterations})
			df2 = pd.DataFrame(data={"Performance Mean": df['Performance'].mean(), "Performance Max": df['Performance'].max(),
				"Performance Min": df['Performance'].min(), "Performance Std": df['Performance'].std(), "Time Mean": df['Time'].mean(), "Time Max": df['Time'].max(),
				"Time Min": df['Time'].min(), "Time Std": df['Time'].std()}, index=[0])
			writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
			df.to_excel(writer, sheet_name='Sheet1')
			df2.to_excel(writer, sheet_name='Sheet2')
			writer.save()
