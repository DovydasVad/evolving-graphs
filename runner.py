from tqdm import tqdm
from algorithms.algorithm import Algorithm

def visualize_result(algorithm: Algorithm, answer_correct: bool):
    print_char = '.'
    if answer_correct:
        if hasattr(algorithm, 'primary_valid') and not algorithm.primary_valid:
            print_char = '_'
    else:
        print_char = 'F'
        if hasattr(algorithm, 'primary_valid') and not algorithm.primary_valid:
            print_char = 'S'
    print(print_char, end = "")


class Runner:
    def __init__(self, probe_rate, change_rate, algorithm, graph, use_dataset = False, dataset = None):
        self.correct_answers = 0
        self.correct_answers_after_1st_phase = 0
        self.total_iterations = 0
        self.probe_rate = probe_rate
        self.change_rate = change_rate
        self.algorithm = algorithm
        self.graph = graph
        self.use_dataset = use_dataset
        self.dataset = dataset
        if use_dataset:
            algorithm.set_start_vertex(dataset["start_vertex"])
            algorithm.set_end_vertex(dataset["end_vertex"])
            graph.set_start_vertex(dataset["start_vertex"])
            graph.set_end_vertex(dataset["end_vertex"])
    
    def run(self, iterations, visualization_step):
        self.total_iterations += iterations
        for iteration in tqdm(range(iterations), disable = (not self.use_dataset)):
            # perform probes
            for j in range(self.probe_rate):
                v = self.algorithm.get_probe_input()
                self.algorithm.set_probe_result(self.graph.probe(v))

            # get and validate answers from models
            answer = self.algorithm.answer()
            answer_correct = (self.graph.validate(answer) == 0)
            if answer_correct:
                self.correct_answers += 1
                if iteration >= self.algorithm.phase_length:
                    self.correct_answers_after_1st_phase += 1
            if visualization_step != -1 and iteration % visualization_step == 0:
                visualize_result(self.algorithm, answer_correct)
            
            # perform changes in the model
            if self.use_dataset:
                if iteration == 0:
                    self.graph.import_edges(self.dataset["edges"][iteration])
                else:
                    self.graph.update_edges(self.dataset["new_edges"][iteration], self.dataset["removed_edges"][iteration])
            else:
                for j in range(self.change_rate):
                    self.graph.change()
    
    def get_total_iterations(self):
        return self.total_iterations

    def get_correct_answers(self):
        return self.correct_answers
    
    def get_correct_answers_after_1st_phase(self):
        return self.correct_answers_after_1st_phase