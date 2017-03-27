from task import Task
import vars

def main():
	train_task = Task()
	train_task._train_rnn()
	train_task._predict_grp()

if __name__ == '__main__':
	main()