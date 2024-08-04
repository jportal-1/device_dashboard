import { authGuardFn } from './helpers/auth.guard';
import { DashboardComponent } from './dashboard/dashboard.component';
import { Routes } from '@angular/router';
import { LoginPageComponent } from './login-page/login-page.component';

export const routes: Routes = [
  {
    path: '',
    component: DashboardComponent,
    canActivate: [authGuardFn]
  },
  {
    path: 'login',
    component: LoginPageComponent
  }
];