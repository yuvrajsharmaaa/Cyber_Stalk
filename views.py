from aquilify.shortcuts import render, redirect

# Define all your views here.

async def homeview(request) -> None:
    return await redirect("/cyberstalking/homepage", 302)