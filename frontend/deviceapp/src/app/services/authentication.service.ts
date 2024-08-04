import { Injectable } from '@angular/core';
import { OAuthService } from 'angular-oauth2-oidc';
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  public lastLoginFailed: Boolean = false;

  constructor(
    private oauthService: OAuthService,
    private router: Router
  ) {}

  public login(username: string, password: string): void {
    this.oauthService.fetchTokenUsingPasswordFlow(
      username,
      password).then((resp) => {
        this.lastLoginFailed = false
        this.router.navigate(['/']);
      }, (resp) => {
        this.lastLoginFailed = true
      })
  }
  
  public logout() {
    this.oauthService.logOut()
    this.router.navigate(['/login']);
  }
  
  public isLoggedIn(): boolean {
    return this.oauthService.hasValidAccessToken()
  }
  
  public getToken(): string | null {
    return this.oauthService.getAccessToken();
  }
}
