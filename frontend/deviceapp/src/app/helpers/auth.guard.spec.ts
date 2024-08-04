import { authGuardFn } from './auth.guard';
import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';


describe('authGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) => 
    TestBed.runInInjectionContext(() => authGuardFn(...guardParameters));

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(executeGuard).toBeTruthy();
  });
});
