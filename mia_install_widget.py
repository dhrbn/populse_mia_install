import os
import yaml
import shutil
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore


class MIAInstallWidget(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        # Labels
        self.top_label_text = 'Welcome to Populse_MIA installation.'
        self.top_label = QtWidgets.QLabel(self.top_label_text)

        self.top_label_font = QtGui.QFont()
        self.top_label_font.setBold(True)
        self.top_label.setFont(self.top_label_font)

        h_box_top_label = QtWidgets.QHBoxLayout()
        h_box_top_label.addStretch(1)
        h_box_top_label.addWidget(self.top_label)
        h_box_top_label.addStretch(1)

        self.middle_label_text = 'Please select an installation path and a folder to store your future projects.'

        self.middle_label = QtWidgets.QLabel(self.middle_label_text)
        h_box_middle_label = QtWidgets.QHBoxLayout()
        h_box_middle_label.addStretch(1)
        h_box_middle_label.addWidget(self.middle_label)
        h_box_middle_label.addStretch(1)

        # Groupbox
        self.groupbox = QtWidgets.QGroupBox()

        mia_path_default = ''  # to determine from the system (ex: for Windows: Program Files)

        self.mia_path_label = QtWidgets.QLabel("Populse_MIA installation path:")
        self.mia_path_choice = QtWidgets.QLineEdit(mia_path_default)
        self.mia_path_browse = QtWidgets.QPushButton("Browse")
        self.mia_path_browse.clicked.connect(self.browse_mia_path)

        self.mia_path_info = QtWidgets.QPushButton(" ? ")
        self.mia_path_info.setFixedHeight(27)
        self.mia_path_info.setFixedWidth(27)
        self.mia_path_info.setStyleSheet("background-color:rgb(150,150,200)")
        rect = QtCore.QRect(4, 4, 17, 17)
        region = QtGui.QRegion(rect, QtGui.QRegion.Ellipse)
        self.mia_path_info.setMask(region)
        tool_tip_message = "Two folders will be created in the selected folder:\n- populse_mia: containing " \
                           "populse_mia's configuration and resources files.\n- MRIFileManager: containing " \
                           "the file converter used in Populse_MIA."
        self.mia_path_info.setToolTip(tool_tip_message)

        h_box_mia_path = QtWidgets.QHBoxLayout()
        h_box_mia_path.addWidget(self.mia_path_choice)
        h_box_mia_path.addWidget(self.mia_path_browse)
        h_box_mia_path.addWidget(self.mia_path_info)

        v_box_mia_path = QtWidgets.QVBoxLayout()
        v_box_mia_path.addWidget(self.mia_path_label)
        v_box_mia_path.addLayout(h_box_mia_path)

        projects_path_default = ''  # setting a default value for the projects?

        self.projects_path_label = QtWidgets.QLabel("Populse_MIA projects path:")
        self.projects_path_choice = QtWidgets.QLineEdit(projects_path_default)
        self.projects_path_browse = QtWidgets.QPushButton("Browse")
        self.projects_path_browse.clicked.connect(self.browse_projects_path)

        self.projects_path_info = QtWidgets.QPushButton(" ? ")
        self.projects_path_info.setFixedHeight(27)
        self.projects_path_info.setFixedWidth(27)
        self.projects_path_info.setStyleSheet("background-color:rgb(150,150,200)")
        rect = QtCore.QRect(4, 4, 17, 17)
        region = QtGui.QRegion(rect, QtGui.QRegion.Ellipse)
        self.projects_path_info.setMask(region)
        tool_tip_message = 'A "projects" folder will be created in this specified folder.'
        self.projects_path_info.setToolTip(tool_tip_message)

        h_box_projects_path = QtWidgets.QHBoxLayout()
        h_box_projects_path.addWidget(self.projects_path_choice)
        h_box_projects_path.addWidget(self.projects_path_browse)
        h_box_projects_path.addWidget(self.projects_path_info)

        v_box_projects_path = QtWidgets.QVBoxLayout()
        v_box_projects_path.addWidget(self.projects_path_label)
        v_box_projects_path.addLayout(h_box_projects_path)

        v_box_paths = QtWidgets.QVBoxLayout()
        v_box_paths.addLayout(v_box_mia_path)
        v_box_paths.addLayout(v_box_projects_path)

        self.groupbox.setLayout(v_box_paths)

        # Push buttons
        self.push_button_install = QtWidgets.QPushButton("Install")
        self.push_button_install.clicked.connect(self.install)

        self.push_button_cancel = QtWidgets.QPushButton("Cancel")
        self.push_button_cancel.clicked.connect(self.close)

        h_box_buttons = QtWidgets.QHBoxLayout()
        h_box_buttons.addStretch(1)
        h_box_buttons.addWidget(self.push_button_install)
        h_box_buttons.addWidget(self.push_button_cancel)

        # Final layout
        self.global_layout = QtWidgets.QVBoxLayout()
        self.global_layout.addLayout(h_box_top_label)
        self.global_layout.addLayout(h_box_middle_label)
        self.global_layout.addWidget(self.groupbox)
        self.global_layout.addLayout(h_box_buttons)

        self.setLayout(self.global_layout)
        self.setWindowTitle("Populse_MIA installation")

    def browse_mia_path(self):
        folder_name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a folder where to install Populse_MIA')
        if folder_name:
            self.mia_path_choice.setText(folder_name)

    def browse_projects_path(self):
        folder_name = QtWidgets.QFileDialog.\
            getExistingDirectory(self, "Select a folder where to store Populse_MIA's projects")
        if folder_name:
            self.projects_path_choice.setText(folder_name)

    def install(self):

        self.folder_exists_flag = False

        # Checking that the specified paths are correct
        mia_path = self.mia_path_choice.text()
        if not os.path.isdir(mia_path):
            message = "The selected path for Populse_MIA must be an existing folder"
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Populse_MIA path is not valid")
            msg.setInformativeText(message)
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.buttonClicked.connect(msg.close)
            msg.exec()
            return

        projects_path = self.projects_path_choice.text()
        if not os.path.isdir(projects_path):
            message = "The selected path for Populse_MIA's projects must be an existing folder"
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Populse_MIA's projects path is not valid")
            msg.setInformativeText(message)
            msg.setWindowTitle("Warning")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.buttonClicked.connect(msg.close)
            msg.exec()
            return

        if os.path.isdir(os.path.join(mia_path, 'populse_mia')):
            message = 'A "populse_mia" folder already exists in the selected path for the populse_mia install'
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText(message)
            self.msg.setInformativeText('By pressing "OK", this folder and its content will be removed.')
            self.msg.setWindowTitle("Warning")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.msg.buttonClicked.connect(self.ok_or_abort)
            self.msg.exec()

        # If the user has clicked on "Cancel" the installation is aborted
        if self.folder_exists_flag:
            return
        else:
            shutil.rmtree(os.path.join(mia_path, 'populse_mia'), ignore_errors=True)

        if os.path.isdir(os.path.join(mia_path, 'MRIFileManager')):
            message = 'A "MRIFileManager" folder already exists in the selected path for the MRIFileManager install'
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText(message)
            self.msg.setInformativeText('By pressing "OK", this folder and its content will be removed.')
            self.msg.setWindowTitle("Warning")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.msg.buttonClicked.connect(self.ok_or_abort)
            self.msg.exec()

        # If the user has clicked on "Cancel" the installation is aborted
        if self.folder_exists_flag:
            return
        else:
            shutil.rmtree(os.path.join(mia_path, 'MRIFileManager'), ignore_errors=True)

        if os.path.isdir(os.path.join(projects_path, 'projects')):
            message = 'A "projects" folder already exists in the selected path for the projects'
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText(message)
            self.msg.setWindowTitle("Warning")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            self.msg.buttonClicked.connect(self.ok_or_abort)
            self.msg.exec()

        # If the user has clicked on "Cancel" the installation is aborted
        if self.folder_exists_flag:
            return

        # Creating a "projects" folder in the specified projects folder
        if not os.path.isdir(os.path.join(projects_path, 'projects')):
            try:
                os.mkdir(os.path.join(projects_path, 'projects'))
            except OSError as e:
                print('Error creating the "projects" folder: ', e)

        # Moving populse_mia folder to the specified location
        self.copy_directory('populse_mia', os.path.join(mia_path, 'populse_mia'))

        # Moving MRIFileManager folder to the specified location
        self.copy_directory('MRIFileManager', os.path.join(mia_path, 'MRIFileManager'))

        # Adding both mia, MRIFileManager and projects paths to Populse_MIA's config
        config_file = os.path.join(mia_path, 'properties', 'config.yml')
        if os.path.isfile(config_file):
            config_dic = self.load_config(config_file)
            config_dic["mia_path"] = os.path.join(mia_path, 'populse_mia')
            config_dic["projects_save_path"] = os.path.join(projects_path, 'projects')
            config_dic["mri_conv_path"] = os.path.join(mia_path, 'MRIFileManager', 'MRIFileManager.jar')
            self.save_config(config_dic, config_file)

        # Installing Populse_MIA's modules using pip
        # self.install_package('populse_mia')  # Not available yet
        subprocess.call(['pip3', 'install', '-i', 'https://test.pypi.org/simple/', 'populse-mia'])

    def ok_or_abort(self, button):
        role = self.msg.buttonRole(button)
        if role == QtWidgets.QMessageBox.AcceptRole:  # "OK" has been clicked
            self.folder_exists_flag = False
        else:
            self.folder_exists_flag = True

    @staticmethod
    def copy_directory(src, dest):
        try:
            shutil.copytree(src, dest)
        # Directories are the same
        except shutil.Error as e:
            print('Directory not copied. Error: %s' % e)
        # Any error saying that the directory doesn't exist
        except OSError as e:
            print('Directory not copied. Error: %s' % e)

    @staticmethod
    def load_config(config_file):
        with open(config_file, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    @staticmethod
    def save_config(config_dic, config_file):
        with open(config_file, 'w', encoding='utf8') as configfile:
            yaml.dump(config_dic, configfile, default_flow_style=False, allow_unicode=True)

    @staticmethod
    def install_package(package):
        import importlib
        try:
            importlib.import_module(package)
        except ImportError:
            import pip
            pip.main(['install', package])
