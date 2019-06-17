export class User{
    isActive:boolean;
    isAdmin:boolean;
    isPrincipal:boolean;
    isStudent:boolean;
    isUser:boolean;
    constructor(
        isActive = false,
        isAdmin = false,
        isPrincipal = false,
        isStudent = false,
        isUser = false
    ){}
}