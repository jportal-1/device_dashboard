import { AuthenticationService } from '../services/authentication.service';
import { Chart } from 'chart.js/auto';
import { CommonModule } from '@angular/common';
import { Component, OnInit, ViewChild } from '@angular/core';
import { environment } from '../environment/environment';
import { HttpClient } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatTable, MatTableModule } from '@angular/material/table';
import 'chartjs-adapter-moment';

export interface ChartPoint {
  x: number;
  y: number;
}

export interface ChartDataSet{
  label: string;
  data: ChartPoint[]
}

export interface TimeSeriesResponse{
  data_point_list: ChartPoint[];
}

export interface DeviceListResponse {
  device_list: string[];
}

export interface DeviceDataResponse {
  device_name: string;
  vibration_velocity: number;
}

export interface DeviceTableEntry {
  name: string;
  velocity: number;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatTableModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  deviceChartData: {datasets: ChartDataSet[]} = {datasets: []}
  deviceChartJS: any;
  deviceChartTimer: any;
  deviceChartUpdateInterval: number = 60;
  deviceChartDisplayedColumns: string[] = ['name', 'velocity'];
  deviceTable: DeviceTableEntry[] = [];
  deviceTableTimer: any
  deviceTableUpdateInterval: number = 5;

  @ViewChild(MatTable) table: any

  constructor(
    private authenticationService: AuthenticationService,
    private http: HttpClient
  ) {}

  // Sort table by device name.
  sortTable() {
    this.deviceTable.sort((a, b) => {
      if (a.name === b.name) {
        return 0;
      } else {
        if (a.name < b.name) {
          return -1;
        }
        return 1;
      }
    });
  }

  // Remove device names, from table, not present anymore in the backend.
  cleanTable(deviceList: string[]) {
    let indexListToDelete: number[] = []
    for (let index = 0; index < this.deviceTable.length; ++index) {
      if (!deviceList.includes(this.deviceTable[index].name)) {
        indexListToDelete.push(index)
      }
    }
    indexListToDelete.reverse()
    for (const index of indexListToDelete) {
      // Note: it is necessary to assign a new value for "this.deviceTable" for it to be redraw correctly in the page.
      this.deviceTable = this.deviceTable.splice(index, 1)
    }
  }

  // Request the latest data of a device.
  requestDeviceTableEntry(deviceName: string) {
    this.http.get<DeviceDataResponse>(environment.apiUrl + "devices/" + deviceName).subscribe({
      next: response => {
        // Adds a new table entry, if it doesn't exist yet for the device, or updates an entry.
        let rowFound = false;
        for (let row of this.deviceTable) {
          if (row.name == deviceName) {
            row.velocity = response.vibration_velocity
            rowFound = true
            break
          }
        }
        if (!rowFound) {
          this.deviceTable.push({name: response.device_name, velocity: response.vibration_velocity})
          this.sortTable()
        }
        this.table.renderRows()
      },  
      error: err => {
        console.error('Error  :', err)
      }
    })
  }

  // Request devices data from backend to update the table.
  requestDeviceTableData() {
    this.http.get<DeviceListResponse>(environment.apiUrl + "devices").subscribe({
      next: response => {
        for (const deviceName of response.device_list) {
          this.requestDeviceTableEntry(deviceName)
        }
        this.cleanTable(response.device_list)
      },
      error: err => {
        console.error('Error:', err)
      }
    })
  }

  // Sort datasets (set of timeseries in this frontend) by device name (present in the label).
  sortDatasetsRows() {
    this.deviceChartData.datasets.sort((a, b) => {
      if (a.label === b.label) {
        return 0;
      } else {
        if (a.label < b.label) {
          return -1;
        }
        return 1;
      }
    });
  }

  // Remove device datasets (timeseries in this frontend) not present anymore in the backend.
  cleanDatasetsRows(deviceList: string[]) {
    let indexListToDelete: number[] = []
    for (let index = 0; index < this.deviceChartData.datasets.length; ++index) {
      if (!deviceList.includes(this.deviceChartData.datasets[index].label)) {
        indexListToDelete.push(index)
      }
    }
    indexListToDelete.reverse()
    for (const index of indexListToDelete) {
      console.log(`Deleting dataset index ${index}`)
      this.deviceChartData.datasets = this.deviceChartData.datasets.splice(index, 1)
    }
  }

  // Request a device timeseries.
  requestDeviceTimeseries(deviceName: string){
    this.http.get<TimeSeriesResponse>(
      // The timeseries requested is from 1 hour ago with 1 minute resolution.
      environment.apiUrl + "devices/" + deviceName + "/timeseries?hours_since=1&resolution=1").subscribe({
      next: response => {
        // Adds a new dataset entry, if the device timeseries doesn't exist yet, or updates an entry.
        let dataSetFound = false;
        for (let dataSet of this.deviceChartData.datasets) {
          if (dataSet.label == deviceName) {
            dataSet.data = response.data_point_list
            dataSetFound = true;
            break
          }
        }
        if (!dataSetFound) {
          this.deviceChartData.datasets.push({label: deviceName, data: response.data_point_list})
          this.sortDatasetsRows();
        }
        this.deviceChartJS.update();
      },  
      error: err => {
        console.error('Error  :', err)
      }
    })
  }

  // Request devices timeseries from backend to update the chart.
  requestDeviceChartData(){
    this.http.get<DeviceListResponse>(environment.apiUrl + "devices").subscribe({
      next: response => {
        for (const deviceName of response.device_list) {
          this.requestDeviceTimeseries(deviceName)
        }
        this.cleanDatasetsRows(response.device_list)

        // Keep a 30 min moving window in time axis by resetting x axis properties.
        let x = {...this.deviceChartJS.options.scales.x};
        x.min = (new Date(Date.now() - 30 * 60000)).toISOString();
        this.deviceChartJS.options.scales.x = x
        this.deviceChartJS.update();
      },
      error: err => {
        console.error('Error:', err)
      }
    })
  }

  ngOnInit(): void {
    this.requestDeviceTableData()
    this.deviceTableTimer = setInterval(this.requestDeviceTableData.bind(this), this.deviceTableUpdateInterval * 1000, this)
    this.requestDeviceChartData()
    this.deviceChartTimer = setInterval(this.requestDeviceChartData.bind(this), this.deviceChartUpdateInterval * 1000, this)

    this.deviceChartJS = new Chart('canvas', {
      type: 'line',
      data: this.deviceChartData,
      options: {
        plugins: {
          colors: {
            forceOverride: true
          }
        },
        scales: {
          x: {
            min: (new Date(Date.now() - 30 * 60000)).toISOString(),
            time: {
              unit: 'minute',
              displayFormats: {
                hour: 'D-M-Y H:00:00'
              },
              tooltipFormat: 'D-M-Y H:00:00',
              minUnit: 'minute',
            },
            title: {
              display: true,
              font: {
                size: 20
              },
              text: "Time"
            },
            type: 'time'
          },
          y: {
            min: 0,
            title: {
              display: true,
              font: {
                size: 20
              },
              text: "Summed Velocity"
            }
          }
        }
      }
    });
  }

  ngOnDestroy(): void {
    clearInterval(this.deviceTableTimer);
    clearInterval(this.deviceChartTimer);
  }

  logout(): void {
    clearInterval(this.deviceTableTimer);
    clearInterval(this.deviceChartTimer);
    this.authenticationService.logout();
  }
}
