""" Define the contents of training panel. """

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
                             QComboBox, QSpinBox, QDoubleSpinBox, QLabel,
                             QProgressBar, QPushButton, QRadioButton,
                             QCheckBox)

from panel import Panel
from testing_panel import TestingPanel
from error_linechart import ErrorLineChart
from rbfn import RBFN
# from ga import GA


class TrainingPanel(Panel):

    def __init__(self, datasets, testing_panel):
        super().__init__()
        if isinstance(testing_panel, TestingPanel):
            self.testing_panel = testing_panel
        else:
            raise TypeError('"testing_panel" must be the instance of '
                            '"TestingPanel"')
        self.datasets = datasets

        self.__set_execution_ui()
        self.__set_options_ui()
        self.__set_outputs_ui()
        self.__set_graphic_ui()

    def __set_execution_ui(self):
        group_box = QGroupBox('Training Execution')
        inner_layout = QHBoxLayout()
        group_box.setLayout(inner_layout)

        self.data_selector = QComboBox()
        self.data_selector.addItems(self.datasets.keys())
        self.data_selector.setStatusTip('Select the training dataset.')

        self.start_btn = QPushButton('Train')
        self.start_btn.setStatusTip('Start training.')
        self.start_btn.clicked.connect(self.__run)

        self.stop_btn = QPushButton('Stop')
        self.stop_btn.setStatusTip('Force the training stop running.')
        self.stop_btn.setDisabled(True)

        self.multicore_cb = QCheckBox('Multicore')
        self.multicore_cb.setStatusTip('Use multiprocessing in calculating '
                                       'fitting for populations.')
        self.multicore_cb.setChecked(True)

        inner_layout.addWidget(self.data_selector, 1)
        inner_layout.addWidget(self.start_btn)
        inner_layout.addWidget(self.stop_btn)
        inner_layout.addWidget(self.multicore_cb)

        self._layout.addWidget(group_box)

    def __set_options_ui(self):
        group_box = QGroupBox('Training Options')
        inner_layout = QFormLayout()
        group_box.setLayout(inner_layout)

        self.iter_times = QSpinBox()
        self.iter_times.setRange(1, 1000000)
        self.iter_times.setValue(300)
        self.iter_times.setStatusTip('The total iterating times for training.')

        self.population_size = QSpinBox()
        self.population_size.setRange(1, 100000000)
        self.population_size.setValue(100)
        self.population_size.setStatusTip('The population size for the PSO.')

        self.nneuron = QSpinBox()
        self.nneuron.setRange(1, 1000)
        self.nneuron.setValue(6)
        self.nneuron.setStatusTip('The number of RBFN neuron.')

        self.sd_max = QDoubleSpinBox()
        self.sd_max.setRange(0.01, 20)
        self.sd_max.setValue(10)
        self.sd_max.setSingleStep(0.1)
        self.sd_max.setStatusTip('The random range maximum of standard '
                                 'deviation of each neuron in RBFN (only for '
                                 'initialization).')

        inner_layout.addRow('Iterating Times:', self.iter_times)
        inner_layout.addRow('Population Size:', self.population_size)
        inner_layout.addRow('Number of Neuron:', self.nneuron)
        inner_layout.addRow('Maximum of SD:', self.sd_max)

        self._layout.addWidget(group_box)

    def __set_outputs_ui(self):
        group_box = QGroupBox('Training Details')
        inner_layout = QFormLayout()
        group_box.setLayout(inner_layout)

        self.current_iter_time = QLabel('--')
        self.current_error = QLabel('--')
        self.avg_error = QLabel('--')
        self.least_error = QLabel('--')
        self.progressbar = QProgressBar()

        self.current_iter_time.setAlignment(Qt.AlignCenter)
        self.current_error.setAlignment(Qt.AlignCenter)
        self.avg_error.setAlignment(Qt.AlignCenter)
        self.least_error.setAlignment(Qt.AlignCenter)

        self.current_iter_time.setStatusTip('The current iterating time of '
                                            'the PSO.')
        self.current_error.setStatusTip('The current error from the fitting '
                                        'function.')
        self.avg_error.setStatusTip('The average error from the fitting '
                                    'function in current iteration.')
        self.least_error.setStatusTip('The least error from the fitting '
                                      'function in training.')

        inner_layout.addRow('Current Iterating Time:', self.current_iter_time)
        inner_layout.addRow('Current Error:', self.current_error)
        inner_layout.addRow('Average Error:', self.avg_error)
        inner_layout.addRow('Least Error:', self.least_error)
        inner_layout.addRow(self.progressbar)

        self._layout.addWidget(group_box)

    def __set_graphic_ui(self):
        group_box = QGroupBox('Error Line Charts:')
        inner_layout = QVBoxLayout()
        group_box.setLayout(inner_layout)

        self.err_chart = ErrorLineChart(1)
        self.err_chart.setStatusTip('The history of error from the fitting '
                                    'of the PSO for each data.')
        self.__err_x = 1

        self.iter_err_chart = ErrorLineChart(2, ('Avg', 'Least'))
        self.iter_err_chart.setStatusTip('The history of average and least '
                                         'error from the fitting of the PSO '
                                         'for each iteration.')
        self.iter_err_chart.setMinimumHeight(150)

        inner_layout.addWidget(QLabel('Current Error'))
        inner_layout.addWidget(self.err_chart)
        inner_layout.addWidget(QLabel('Average Error'))
        inner_layout.addWidget(self.iter_err_chart)
        self._layout.addWidget(group_box)

    @pyqtSlot()
    def __init_widgets(self):
        self.start_btn.setDisabled(True)
        self.stop_btn.setEnabled(True)
        self.multicore_cb.setDisabled(True)
        self.data_selector.setDisabled(True)
        self.iter_times.setDisabled(True)
        self.population_size.setDisabled(True)
        self.score_amplifier.setDisabled(True)
        self.roulette_wheel_selection.setDisabled(True)
        self.tournament_selection.setDisabled(True)
        self.p_crossover.setDisabled(True)
        self.p_mutation.setDisabled(True)
        self.mutation_scale.setDisabled(True)
        self.nneuron.setDisabled(True)
        self.sd_max.setDisabled(True)
        self.err_chart.clear()
        self.iter_err_chart.clear()
        self.__err_x = 1

    @pyqtSlot()
    def __reset_widgets(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setDisabled(True)
        self.multicore_cb.setEnabled(True)
        self.data_selector.setEnabled(True)
        self.iter_times.setEnabled(True)
        self.population_size.setEnabled(True)
        self.score_amplifier.setEnabled(True)
        self.roulette_wheel_selection.setEnabled(True)
        self.tournament_selection.setEnabled(True)
        self.p_crossover.setEnabled(True)
        self.p_mutation.setEnabled(True)
        self.mutation_scale.setEnabled(True)
        self.nneuron.setEnabled(True)
        self.sd_max.setEnabled(True)

    @pyqtSlot(int)
    def __show_current_iter_time(self, value):
        self.current_iter_time.setText(str(value + 1))
        self.progressbar.setValue(value + 1)

    @pyqtSlot(float)
    def __show_current_error(self, value):
        self.current_error.setText('{:.7f}'.format(value))
        self.err_chart.append_point(self.__err_x, value)
        self.__err_x += 1

    @pyqtSlot(float, float)
    def __show_iter_error(self, avg, least):
        self.avg_error.setText('{:.7f}'.format(avg))
        self.least_error.setText('{:.7f}'.format(least))
        self.iter_err_chart.append_point(
            int(self.current_iter_time.text()), least, 1)
        self.iter_err_chart.append_point(
            int(self.current_iter_time.text()), avg, 0)

    def __run(self):
        self.progressbar.setMaximum(self.iter_times.value())

        self.__current_dataset = self.datasets[self.data_selector.currentText(
        )]
        mean_range = (min(min(d.i) for d in self.__current_dataset),
                      max(max(d.i) for d in self.__current_dataset))

        rbfn = RBFN(self.nneuron.value(), mean_range, self.sd_max.value())

        # self.__ga = GA(self.iter_times.value(), self.population_size.value(),
        #                reproduction_method,
        #                self.p_crossover.value(), self.p_mutation.value(),
        #                self.mutation_scale.value(), rbfn,
        #                self.__current_dataset, mean_range, self.sd_max.value(),
        #                score_amplifier=self.score_amplifier.value(),
        #                is_multicore=self.multicore_cb.isChecked())
        # self.stop_btn.clicked.connect(self.__ga.stop)
        # self.__ga.started.connect(self.__init_widgets)
        # self.__ga.finished.connect(self.__reset_widgets)
        # self.__ga.sig_current_iter_time.connect(self.__show_current_iter_time)
        # self.__ga.sig_current_error.connect(self.__show_current_error)
        # self.__ga.sig_iter_error.connect(self.__show_iter_error)
        # self.__ga.sig_console.connect(self.testing_panel.print_console)
        # self.__ga.sig_rbfn.connect(self.testing_panel.load_rbfn)
        # self.__ga.start()
