import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() {}

  isLoggedIn(): boolean {
    return !!localStorage.getItem('auth_token'); 
  }

  setAuthToken(token: string): void {
    localStorage.setItem('auth_token', token); 
  }

  
  logout(): void {
    localStorage.removeItem('auth_token');
  }
}
