import { TestBed, inject } from '@angular/core/testing';

import { SchoolApiService } from './school-api.service';

describe('SchoolApiService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [SchoolApiService]
    });
  });

  it('should be created', inject([SchoolApiService], (service: SchoolApiService) => {
    expect(service).toBeTruthy();
  }));
});
