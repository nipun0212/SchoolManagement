import { TestBed, inject } from '@angular/core/testing';

import { PrincipleGuardService } from './principle-guard.service';

describe('PrincipleGuardService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [PrincipleGuardService]
    });
  });

  it('should be created', inject([PrincipleGuardService], (service: PrincipleGuardService) => {
    expect(service).toBeTruthy();
  }));
});
