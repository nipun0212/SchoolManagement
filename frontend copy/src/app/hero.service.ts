import { Injectable } from '@angular/core';
import {Hero} from './hero';
import {HEROES} from './mock-heroes';
import {Http} from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { Observable }     from 'rxjs/Observable';
import 'rxjs/add/operator/map';
// import {GoogleApiService} from "ng-gapi";

@Injectable()
export class HeroService {
  constructor(private http:Http) {

    // gapiService.onLoad(()=> {
    //   gapi.load('client',()=>
    //   gapi.load('auth2',()=>console.log("Nipun")))});

   }
  private heroesUrl = 'api/heroes';
  private headers = new Headers({'Content-Type': 'application/json'});
  
  getHeroesSlowly():Promise<Hero[]>{

    return new Promise(resolve =>{

      setTimeout(()=>resolve(this.getHeroes()),0)

    } 
    )
    
  }
  // getHeroes():Hero[]{
  // return HEROES;
  // }

  // getHero(id:number):Promise<Hero>{
  //   return this.getHeroesSlowly().then(heroes=> heroes.find(hero=>hero.id ===id));
  // }

  getHeroes():Promise<Hero[]>{
    return this.http.get(this.heroesUrl)
      .toPromise()
      .then(response=> response.json().data as Hero[])
      .catch(this.handleError);
      
      
  }

  private handleError(error:any):Promise<any>{
    console.error('an error occured',error);
    return Promise.reject(error.message||error);
  }

  getHero(id:number):Promise<Hero>{
    const url = this.heroesUrl + '/' + id;
    return this.http.get(url)
      .toPromise()
      .then(response=>response.json().data as Hero)
      .catch(this.handleError);
  }

update(hero:Hero):Promise<Hero>{
  const url = this.heroesUrl + '/' + hero.id;
  return this.http
  .put(url,JSON.stringify(hero))
  .toPromise()
  .then(()=>hero)
  .catch(this.handleError);
}

create(name:string):Promise<Hero>{
  return this.http
    .post(this.heroesUrl,JSON.stringify({name:name}))
    .toPromise()
    .then(res=>res.json().data as Hero)
    .catch(this.handleError)
}

delete(id:number):Promise<void>{
  const url = this.heroesUrl + '/' + id;
  return this.http
    .delete(url)
    .toPromise()
    .then(()=>null)
    .catch(this.handleError)
}

search(term:string):Observable<Hero[]>{

  const url = this.heroesUrl + '/?name=' + term;

  return this.http
    .get(url)
    .map(res=>res.json().data as Hero[]);
}

}
