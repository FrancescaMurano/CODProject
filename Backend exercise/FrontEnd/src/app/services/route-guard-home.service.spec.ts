import { TestBed } from '@angular/core/testing';

import { RouteGuardHomeService } from './route-guard-home.service';

describe('RouteGuardHomeService', () => {
  let service: RouteGuardHomeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RouteGuardHomeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
