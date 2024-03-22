from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import logout
from .models import Candidate, UserVoteStatus
from django.contrib.auth.decorators import login_required

from Voting.forms import StudentRegistrationForm

# Create your views here.
def index(request):
    return render(request,'index.html')


# register function
def register(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been Created')
            return redirect('login')
    else:
        form = StudentRegistrationForm()

    return render(request, 'register.html', {'form': form})




# logout function
@login_required
def logout_view(request):
    logout(request)
    return redirect("index")



@login_required
def submit_vote(request):
    user = request.user
    
    # Check if the user has already voted
    if UserVoteStatus.objects.filter(user=user).exists():
        messages.error(request, 'You have already voted.')
        return redirect('vote')
    
    if request.method == 'POST':
        positions = ['president', 'vice_president', 'finance_secretary', 'academic_secretary', 'delegate']
        selected_positions = set(request.POST.keys()) & set(positions)
        
        if len(selected_positions) == len(positions):
            for position in selected_positions:
                candidate_id = request.POST.get(position)
                if candidate_id:
                    try:
                        candidate = Candidate.objects.get(pk=candidate_id)
                        candidate.votes += 1
                        candidate.save()
                    except Candidate.DoesNotExist:
                        messages.error(request, f'Candidate for {position.replace("_", " ").title()} does not exist.')
                        return redirect('vote')

            # Create a UserVoteStatus object to mark the user as voted
            UserVoteStatus.objects.create(user=user)
            
            messages.success(request, 'Your vote has been submitted successfully!')
            return redirect('results')
        else:
            messages.error(request, 'Please select candidates for all positions.')
            return redirect('vote')
    else:
        messages.error(request, 'Invalid request!')
        return redirect('vote')
    




@login_required
def results(request):
    # Fetch all candidates
    all_candidates = Candidate.objects.all()

    # Dictionary to store position-wise total votes
    position_totals = {}

    # Calculate total votes for each position
    for candidate in all_candidates:
        position_totals.setdefault(candidate.position, 0)
        position_totals[candidate.position] += candidate.votes

    # Calculate vote percentage for each candidate
    for candidate in all_candidates:
        if position_totals[candidate.position] > 0:
            candidate.vote_percentage = round((candidate.votes / position_totals[candidate.position]) * 100, 2)
        else:
            candidate.vote_percentage = 0  # Avoid division by zero

    return render(request, 'result.html', {'candidates': all_candidates})



@login_required
def vote(reqeust):
    candidates=Candidate.objects.all()
    context={
        'candidates':candidates
    }
    return render(reqeust,'vote.html',context)