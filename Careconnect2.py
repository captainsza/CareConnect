import sys
from PyQt5.QtWidgets import QProgressBar,QWidget,QApplication, QMainWindow,QCheckBox, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis
from PyQt5.QtCore import Qt,QTimer
from PyQt5.QtGui import QPainter,QBrush,QColor
import csv

class HospitalManagementAnalytics(QMainWindow):
    STAFF_COL = 1
    DOCTORS_COL = 2
    BEDS_COL = 3
    CT_SCANNERS_COL = 4
    MRI_MACHINES_COL = 5
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Hospital Management Analytics")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icon.png"))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_resources)
        self.timer.start(3000)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Hospital Name", "Number of Staff", "Number of Doctors", "Number of Beds", "Number of CT Scanners", "Number of MRI Machines"])
        self.table.setMinimumWidth(800)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setStyleSheet("QTableWidget {background-color: #F0F8FF;}")
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

    # Load data from CSV file
        with open("demo_data.csv", "r") as file:
            reader = csv.reader(file)
            next(reader) # Skip the first row (header)
            for row_index, row in enumerate(reader):
                self.table.insertRow(row_index)
                for col_index, col in enumerate(row):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(col))

    # Create buffer storage input and label
        self.buffer_label = QLabel("Buffer Storage:")
        self.buffer_input = QLineEdit()

    
    # Create transfer resources button
        self.transfer_button = QPushButton("Transfer Resources")
        self.transfer_button.clicked.connect(self.transfer_resources)
    # Add search bar and button
        self.search_bar = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.handle_search)
    
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setRenderHint(QPainter.NonCosmeticDefaultPen)
        self.chart_view.setRenderHint(QPainter.Qt4CompatiblePainting)
        self.chart_view.setRenderHint(QPainter.TextAntialiasing)
        self.chart_view.setBackgroundBrush(QBrush(QColor(240, 248, 255)))
        self.chart_view.chart().setTheme(QChart.ChartThemeLight)
        self.checkbox_layout = QVBoxLayout()
   
    # Create a horizontal layout for buffer and button
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.buffer_label)
        h_layout.addWidget(self.buffer_input)
        h_layout.addWidget(self.transfer_button)
        h_layout.addStretch()
    
    # Create a grid layout for table and checkbox layout
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.table,0,0)
        grid_layout.addWidget(self.search_bar,1,0)
        grid_layout.addWidget(self.search_button,1,1)
        grid_layout.addLayout(h_layout,2,0)
        grid_layout.addWidget(self.chart_view,3,0,1,2)
    
    # Create a central widget to hold the layouts
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)

    def handle_search(self):
        search_text = self.search_bar.text()
        for i in range(self.table.rowCount()):
            hospital_name = self.table.item(i, 0).text()
            if search_text.lower() in hospital_name.lower():
                self.table.showRow(i)
            else:
                self.table.hideRow(i)

    def transfer_resources(self):
        pass

    def check_resources(self):
        pass

    def update_chart(self):
        pass

    def check_resources(self):
        # Define threshold level
        threshold = 10

        # Check resources for each row in the table
        for row in range(self.table.rowCount()):
            staff = int(self.table.item(row, self.STAFF_COL).text())
            if staff < threshold:
                # Transfer resources from other hospitals to this hospital
                for other_row in range(self.table.rowCount()):
                    if other_row != row:
                        # Get resources from other hospital
                        staff_to_transfer = int(self.table.item(other_row, self.STAFF_COL).text()) - threshold
                        # Update resources in other hospital
                        self.table.item(other_row, self.STAFF_COL).setText(str(staff_to_transfer))
                        # Update resources in current hospital
                        self.table.item(row, self.STAFF_COL).setText(str(staff + staff_to_transfer))
                        break
        self.init_chart()

    def init_chart(self):
        # Create chart
        self.chart = QChart()
        self.chart.setTitle("Resource Percentage in Hospitals")
        
        # Create bar series
        self.bar_series = QBarSeries()
        
        # Add data to bar series
        for row in range(self.table.rowCount()):
            # Create bar set for each hospital
            bar_set = QBarSet(self.table.item(row, 0).text())
            
            # Calculate resource percentage
            try:
                staff = int(self.table.item(row, self.STAFF_COL).text())
            except ValueError:
                continue

            total_resources = staff + int(self.table.item(row, 2).text()) + int(self.table.item(row, 3).text()) + int(self.table.item(row, 4).text()) + int(self.table.item(row, 5).text())
            staff_percent = (staff / total_resources) * 100
            
            # Add data to bar set
            bar_set.append(staff_percent)
            
            # Add bar set to series
            self.bar_series.append(bar_set)
        
        # Set bar series to chart
        self.chart.addSeries(self.bar_series)
        
        # Create category axis
        self.category_axis = QBarCategoryAxis()
        self.category_axis.append("Hospitals")
        
        # Set category axis to chart
        self.chart.createDefaultAxes()
        self.chart.setAxisX(self.category_axis, self.bar_series)
        
        
        
        # Set chart to chart view
        self.chart_view.setChart(self.chart)
    def update_chart(self):
        # Create a new bar series
        bar_series = QBarSeries()
        # Add data to bar series based on selected checkboxes
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.isChecked():
                # Create bar set for selected hospital
                bar_set = QBarSet(self.table.item(i, 0).text())
                # Calculate resource percentage
                staff = int(self.table.item(i, 1).text())
                total_resources = staff + int(self.table.item(i, 2).text()) + int(self.table.item(i, 3).text()) + int(self.table.item(i, 4).text()) + int(self.table.item(i, 5).text())
                staff_percent = (staff / total_resources) * 100
                # Add data to bar set
                bar_set.append(staff_percent)
                # Add bar set to series
                bar_series.append(bar_set)
        # Set bar series to chart
        self.chart.removeAllSeries()
        self.chart.addSeries(bar_series)
        self.chart.createDefaultAxes()
    # Example setData method for staff_chart_view
    def setData(self, data):
        series = QBarSeries()
        set = QBarSet("Staff")
        set.append(data)
        series.append(set)
        self.chart().addSeries(series)
        self.chart().createDefaultAxes()
        self.chart().axisX().setRange(0, data + 5)
        self.chart().axisY().setRange(0, data + 5)
 

    def transfer_resources(self):
        # Enable multiple row selection
        self.table.setSelectionMode(QTableWidget.MultiSelection)
        selected_indexes = self.table.selectedIndexes()
        # Check if two rows are selected
        if len(selected_indexes) != 2:
            print("Please select source and destination hospital")
            return
        source_row = selected_indexes[0].row()
        destination_row = selected_indexes[1].row()


        # Get buffer storage value
        buffer_input = self.buffer_input.text()
        if buffer_input == "":
            # Display error message or prompt to user
            self.buffer_input.setStyleSheet("border: 1px solid red;")
            self.buffer_input.setPlaceholderText("Please enter a valid buffer storage value")
            return

        buffer = int(buffer_input)
        self.buffer_input.setStyleSheet("")
        self.buffer_input.setPlaceholderText("")

        # Get resource columns
        staff_col = 1
        doctors_col = 2
        beds_col = 3
        ct_scanners_col = 4
        mri_machines_col = 5

        # Transfer resources
        staff = int(self.table.item(source_row, staff_col).text()) - buffer
        self.table.item(source_row, staff_col).setText(str(staff))
        self.table.item(destination_row, staff_col).setText(str(int(self.table.item(destination_row, staff_col).text()) + buffer))

        doctors = int(self.table.item(source_row, doctors_col).text()) - buffer
        self.table.item(source_row, doctors_col).setText(str(doctors))
        self.table.item(destination_row, doctors_col).setText(str(int(self.table.item(destination_row, doctors_col).text()) + buffer))
        beds = int(self.table.item(source_row, beds_col).text()) - buffer
        self.table.item(source_row, beds_col).setText(str(beds))
        self.table.item(destination_row, beds_col).setText(str(int(self.table.item(destination_row, beds_col).text()) + buffer))

        ct_scanners = int(self.table.item(source_row, ct_scanners_col).text()) - buffer
        self.table.item(source_row, ct_scanners_col).setText(str(ct_scanners))
        self.table.item(destination_row, ct_scanners_col).setText(str(int(self.table.item(destination_row, ct_scanners_col).text()) + buffer))

        mri_machines = int(self.table.item(source_row, mri_machines_col).text()) - buffer
        self.table.item(source_row, mri_machines_col).setText(str(mri_machines))
        self.table.item(destination_row, mri_machines_col).setText(str(int(self.table.item(destination_row, mri_machines_col).text()) + buffer))
                # Create resource labels and progress bars
        self.staff_label = QLabel("Staff:")
        self.staff_bar = QProgressBar()
        self.doctors_label = QLabel("Doctors:")
        self.doctors_bar = QProgressBar()
        self.beds_label = QLabel("Beds:")
        self.beds_bar = QProgressBar()
        self.ct_scanners_label = QLabel("CT Scanners:")
        self.ct_scanners_bar = QProgressBar()
        self.mri_machines_label = QLabel("MRI Machines:")
        self.mri_machines_bar = QProgressBar()

        # Add resource labels and progress bars to layout
        resources_layout = QVBoxLayout()
        resources_layout.addWidget(self.staff_label)
        resources_layout.addWidget(self.staff_bar)
        resources_layout.addWidget(self.doctors_label)
        resources_layout.addWidget(self.doctors_bar)
        resources_layout.addWidget(self.beds_label)
        resources_layout.addWidget(self.beds_bar)
        resources_layout.addWidget(self.ct_scanners_label)
        resources_layout.addWidget(self.ct_scanners_bar)
        resources_layout.addWidget(self.mri_machines_label)
        resources_layout.addWidget(self.mri_machines_bar)
        self.setLayout(resources_layout)
        self.init_chart()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    analytics = HospitalManagementAnalytics()
    analytics.show()
    sys.exit(app.exec_())

    





