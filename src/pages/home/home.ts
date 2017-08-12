import { Component } from '@angular/core'
import { LoadingController, NavController} from 'ionic-angular'
import { IXLuncApi } from "../../common/ix-lunch-api.service"
import { Geolocation, Geoposition } from '@ionic-native/geolocation';
import { NativeGeocoder, NativeGeocoderReverseResult } from '@ionic-native/native-geocoder';
 

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {
 luncMenu: any
 rating: any
 myLocation : any
 currentDate = new Date();
 
  
  constructor(
      public nav: NavController, 
      public eliteApi: IXLuncApi,
      public loadingController: LoadingController,
      public geolocation: Geolocation, 
      public geocoder: NativeGeocoder
      ) { }


  ionViewDidLoad(){
    //this.geolocate()
   this.getMenu(this.myLocation,this.currentDate)
  }
  
  showRatingFunc(userRating: any): boolean {
    if(userRating === 0) {
      return true
    } else {
      return false
    }
  }

  getNextDayMenu(): void {
    this.currentDate.setDate(this.currentDate.getDate() + 1);
    console.log(this.currentDate);
    let loader = this.loadingController.create({
      content: 'Getting lunch menu...'
      //spinner: 'dots'
    });

    loader.present().then(() => {
      this.eliteApi.getLunchMenu(this.myLocation,this.currentDate).then(data => {
        this.luncMenu = [data]
        loader.dismiss()
      });
    });
  }

  onModelChange(event: any, id:any): void {
    console.log("show rating and idt")
    console.log(event);
    console.log(id);
    this.eliteApi.addRating({id: id, rating: event});
  }

  swipeLeftEvent(event: any){
    this.currentDate.setDate(this.currentDate.getDate() + 1);
    //this.getMenuNextDay(this.myLocation, this.currentDate);
    this.getMenu(this.myLocation, this.currentDate);
  }

  swipeRightEvent(event: any){
    this.currentDate.setDate(this.currentDate.getDate() - 1);
    //this.getMenuPreviousDay(this.myLocation, this.currentDate);
    this.getMenu(this.myLocation, this.currentDate);
  }

  doRefresh(event: any) {
    let today = new Date();
    this.eliteApi.getLunchMenu(this.myLocation, today.toISOString().slice(0,10)).
    then(data => {
        this.luncMenu = data
    })

      if(event != 0) {
         event.complete();
      }
  }

   geolocate() {
    let options = {
      enableHighAccuracy: true,
      timout:15000
    };
    
      this.geolocation.getCurrentPosition(options).then((position: Geoposition) => {
      this.getcountry(position);
    }).catch((err) => {
      alert(err);
    }) 
  }

  getMenu(location: any, currentDate: any ) {
    let loader = this.loadingController.create({
      content: 'Getting lunch menu...'
      //spinner: 'dots'
    });

    loader.present().then(() => {
      this.eliteApi.getLunchMenu(location,currentDate.toISOString().slice(0,10)).then(data => {
        this.luncMenu = data
        loader.dismiss()
      });
    });
      
  }

  getMenuNextDay(location: any, currentDate: any ) {
    let loader = this.loadingController.create({
      content: 'Getting lunch menu...'
      //spinner: 'dots'
    });

    loader.present().then(() => {
      this.eliteApi.getLunchMenuNextDay(location,currentDate.toISOString().slice(0,10)).then(data => {
        this.luncMenu = data
        console.log(JSON.stringify(this.luncMenu))
        loader.dismiss()
      });
    });
      
  }

  getMenuPreviousDay(location: any, currentDate: any ) {
    let loader = this.loadingController.create({
      content: 'Getting lunch menu...'
      //spinner: 'dots'
    });

    loader.present().then(() => {
      this.eliteApi.getLunchMenuPreviousDay(location,currentDate.toISOString().slice(0,10)).then(data => {
        this.luncMenu = data
        console.log(JSON.stringify(this.luncMenu))
        loader.dismiss()
      });
    });
      
  }
 
  getcountry(pos) {
    this.geocoder.reverseGeocode(pos.coords.latitude, pos.coords.longitude).then((res: NativeGeocoderReverseResult) => { 
    this.myLocation = res.city;
    this.getMenu(this.myLocation,this.currentDate);
    })
  } 

}
