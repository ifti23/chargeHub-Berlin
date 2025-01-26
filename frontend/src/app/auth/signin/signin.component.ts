import { Component, NgModule } from '@angular/core';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http'; 
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-signin',
  imports: [CommonModule, FormsModule, HttpClientModule], 
  providers: [],
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css'],
})
export class SigninComponent {
  email: string = '';
  password: string = '';
  

  constructor(private http: HttpClient, 
    private router: Router,
    private authService:AuthService) {}
  onSubmit() {
    const apiUrl = 'http://127.0.0.1:5000/api/login_user/';
    const credentials = { username: this.email, password: this.password };
    
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
  
    this.http.post(apiUrl, credentials, { headers }).subscribe({
      next: (response: any) => {
        console.log('Sign in successful', response);
        this.authService.setAuthToken(response.token);
        this.router.navigate(['/searchbypostalcode']);
      },
      error: (err) => {
        console.error('Sign in failed', err);
        alert('Invalid email or password. Please try again.');
      },
    });
  }
  
}