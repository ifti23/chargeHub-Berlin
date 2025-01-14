import { Component } from '@angular/core';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-signup',
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css'],
})
export class SignupComponent {
  username: string = '';
  email: string = '';
  phone: string = '';
  password: string = '';

  constructor(private http: HttpClient, private router: Router) {}

  onSubmit() {
    const apiUrl = 'http://127.0.0.1:5000/api/register_user/';
    console.log('Form submitted', this.username, this.email, this.phone, this.password);

    
    const userCredentials = {
      username: this.username,
      email: this.email,
      phone: this.phone,
      password: this.password,
    };

    
    console.log('Signup credentials:', userCredentials);

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    this.http.post(apiUrl, userCredentials, { headers }).subscribe({
      next: (response: any) => {
        console.log('Sign up successful', response);
        this.router.navigate(['/signin']);
      },
      error: (err) => {
        console.error('Sign up failed', err);
        alert('Signup failed. Please try again.');
      },
    });
  }
}
