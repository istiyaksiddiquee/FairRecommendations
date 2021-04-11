import { HttpClient } from '@angular/common/http';
import { LandingService } from './landing.service';
import { Component, OnInit } from '@angular/core';


@Component({
    selector: 'app-landing',
    templateUrl: './landing.component.html',
    styleUrls: ['./landing.component.scss']
})

export class LandingComponent implements OnInit {
  simpleSlider = 40;
  page = 3;
  focus: any;
  focus1: any;

  constructor(private landingService: LandingService) { }

  ngOnInit() {}

  clickResponse() {
    var infoDiv = document.getElementById('infoDiv');
    infoDiv.hidden === true ? infoDiv.hidden = false : infoDiv.hidden = true;
    this.landingService.getInformation().subscribe((data: any) => {
      console.log(data.research_interests)
    });
  }

  // getInformation() {
  //       try {
  //           return this.http.get(this.URL);
  //       } catch(err) {
  //           console.log(err);
  //       }
  //   }
}
