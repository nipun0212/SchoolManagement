import { TestBed, inject } from '@angular/core/testing';

import { StudentGuardService } from './student-guard.service';

describe('StudentGuardService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [StudentGuardService]
    });
  });

  it('should be created', inject([StudentGuardService], (service: StudentGuardService) => {
    expect(service).toBeTruthy();
  }));
});
