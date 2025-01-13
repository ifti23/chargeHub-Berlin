import { AfterViewInit, Component } from '@angular/core';
import * as L from 'leaflet';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-map',
  imports: [CommonModule, FormsModule],
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements AfterViewInit {
  map!: L.Map;
  postalCode: string = '';
  stations: Array<any> = [];
  
  // Example postal code boundaries (dummy data for demonstration)
  postalCodeBoundaries: any = {
    '10115': [
      [52.5300, 13.4000],
      [52.5310, 13.4020],
      [52.5320, 13.4030],
      [52.5300, 13.4050],
    ],
    '10243': [
      [52.5200, 13.4100],
      [52.5210, 13.4120],
      [52.5220, 13.4130],
      [52.5200, 13.4150],
    ]
  };

  ngAfterViewInit(): void {
    // Initialize the map centered on Berlin
    this.map = L.map('map').setView([52.52, 13.405], 13); // Berlin coordinates (Lat, Lng)

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap contributors'
    }).addTo(this.map);

    // Example station data
    this.stations = [
      { name: 'Station 1', lat: 52.5200, lng: 13.4050, status: 'Available' },
      { name: 'Station 2', lat: 52.5300, lng: 13.4100, status: 'In Use' },
      { name: 'Station 3', lat: 52.5100, lng: 13.4000, status: 'Under Maintenance' }
    ];

    // Display initial stations on the map
    this.displayStationsOnMap(this.stations);
  }

  // Display stations on the map
  displayStationsOnMap(stations: Array<any>): void {
    stations.forEach(station => {
      const marker = L.marker([station.lat, station.lng]).addTo(this.map);
      marker.bindPopup(`<b>${station.name}</b><br>Status: ${station.status}`);
    });
  }

  // Highlight the area for the provided postal code
  highlightArea(postalCode: string): void {
    // Clear existing polygons
    this.map.eachLayer(layer => {
      if ((layer as any).options?.color) {
        this.map.removeLayer(layer); // Remove previously drawn polygons
      }
    });

    // Check if the postal code has a corresponding boundary
    const boundary = this.postalCodeBoundaries[postalCode];
    if (boundary) {
      const polygon = L.polygon(boundary, {
        color: 'blue', // Set the color for the highlighted area
        fillOpacity: 0.3, // Semi-transparent fill
        weight: 2, // Border weight
      }).addTo(this.map);
      
      // Optionally, zoom to the highlighted area
      this.map.fitBounds(polygon.getBounds());
    } else {
      console.log(`No boundary found for postal code: ${postalCode}`);
    }
  }

  // Handle the search form
  onSearch(): void {
    console.log(`Searching for postal code: ${this.postalCode}`);
    
    // Highlight the area based on the entered postal code
    this.highlightArea(this.postalCode);
  }
}
