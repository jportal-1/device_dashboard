import { Component } from '@angular/core';
import { environment } from './environment/environment';
import { OAuthService } from 'angular-oauth2-oidc';
import { RouterOutlet } from '@angular/router';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent {
  title = 'deviceapp';

  constructor(private oauthService: OAuthService) {
    this.oauthService.tokenEndpoint = environment.apiUrl + "auth/token";
    this.oauthService.userinfoEndpoint = environment.apiUrl + "auth/userinfo";
    this.oauthService.clientId = "";
    this.oauthService.scope = "";
    this.oauthService.dummyClientSecret = "";
    this.oauthService.oidc = false;
    this.oauthService.requireHttps = false;
  }
}
