import { Component, AfterViewInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import L from 'leaflet';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-search',
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements AfterViewInit {
  postalCode: string = '';
  stations: any[] = [];
  errorMessage: string = '';
  noStationsFound: boolean = false;
  map!: L.Map;
  STATUS_OPTIONS = ["Operational", "Used", "Malfunctioning"];
  constructor(private http: HttpClient) {}

  ngAfterViewInit(): void {
    
    this.map = L.map('map').setView([52.52, 13.405], 13); 

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap contributors'
    }).addTo(this.map);
  }

  onSubmit(): void {
    const apiUrl = `http://127.0.0.1:5000/api/charging_stations/postal_code/${this.postalCode}`;
  
    this.errorMessage = '';
    this.noStationsFound = false;
  
    this.http.get(apiUrl).subscribe({
      next: (response: any) => {
        this.stations = response.map((station: any) => ({
          ...station,
          status: this.mapFunctionalToStatus(station.functional),
          newStatus: this.mapFunctionalToStatus(station.functional),
        }));
        console.log('Stations:', response);
        if (this.stations.length === 0) {
          this.noStationsFound = true;
        } else {
          this.displayStationsOnMap(this.stations);
        }
      },
      error: (error) => {
        if (error.status === 404) {
          this.errorMessage = 'Failed to fetch charging stations. Please try again.';
          this.stations = [];
          this.displayStationsOnMap(this.stations);
        } else {
          this.errorMessage = 'An error occurred. Please try again.';
        }
        console.error(error);
      },
    });
  }

  displayStationsOnMap(stations: any[]): void {

    this.map.eachLayer(layer => {
      if ((layer as any).options?.pane === 'markerPane') {
        this.map.removeLayer(layer);
      }
    });

    stations.forEach(station => {
      const marker = L.marker([station.latitude, station.longitude]).addTo(this.map);
    
     
      marker.bindPopup(`
        <b>${station.name || 'Charging Station'}</b><br>
        Address: ${station.street || 'N/A'} ${station.house_number || ''}<br>
        Status: ${station.status || 'N/A'}<br>
      `);
    });

    const bounds = L.latLngBounds(stations.map(station => [station.latitude, station.longitude]));
    this.map.fitBounds(bounds);
  }

  mapFunctionalToStatus(functional: string): string {
    if (functional === 'operational') {
      return 'Operational';
    } else if (functional === 'used') {
      return 'Used';
    } else if (functional === 'malfunctioning') {
      return 'Malfunctioning';
    }
    return 'Unknown';
  }

  updateStationStatus(station: any) {
    const apiUrl = `http://127.0.0.1:5000/api/charging_stations/change_status?station_id=${station.id}&new_status=${station.newStatus.toLowerCase()}`;
    
    this.http.post(apiUrl, {}).subscribe({
      next: () => {
        station.status = station.newStatus; 
        console.log(`Station ID ${station.id} updated to ${station.newStatus}`);
      },
      error: (err) => {
        console.error('Error updating station status:', err);
        alert('Failed to update station status. Please try again.');
      }
    });
  }
}
