import {AwesomePipe} from './awesome.pipe';
import {HighlightDirective} from './highlight.directive';
import {ContactService} from './contact.service';
import { NgModule }           from '@angular/core';
import { CommonModule }       from '@angular/common';
import { FormsModule }        from '@angular/forms';
import
{ ContactComponent }   from './contact.component';

@NgModule({
    declarations: [
      AwesomePipe,
      ContactComponent,
      HighlightDirective
    ],
    imports: [
        CommonModule,
        FormsModule
    ],
    providers: [ContactService],
    exports:      [ ContactComponent ]
  })
  export class ContactModule { }