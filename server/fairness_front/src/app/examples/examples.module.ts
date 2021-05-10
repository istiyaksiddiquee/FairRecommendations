import { LandingService } from './landing/landing.service';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NouisliderModule } from 'ng2-nouislider';
import { HttpClientModule } from '@angular/common/http';

import { LandingComponent } from './landing/landing.component';

import {AutocompleteLibModule} from 'angular-ng-autocomplete';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        NgbModule,
        NouisliderModule,
        AutocompleteLibModule,
        HttpClientModule,
    ],
    declarations: [
        LandingComponent,
    ],
    providers: [
        LandingService,
    ]
})
export class ExamplesModule { }
