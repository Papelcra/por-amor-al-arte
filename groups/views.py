from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import GroupForm
from .models import Group

@login_required
def crear_grupo(request):
    # Verificación de rol del usuario
    if request.user.role != 'group_admin':
        return redirect('core:home')

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            form.save_m2m()

            # Validación de miembros únicos
            miembros = form.cleaned_data.get('members', [])
            group.members.clear()
            for artista in miembros:
                if not Group.objects.filter(members=artista).exists():
                    group.members.add(artista)
            
            return redirect('groups:mis_grupos')
    else:
        form = GroupForm()

    return render(request, 'groups/crear.html', {'form': form})

def lista_grupos(request):
    grupos = Group.objects.all()
    return render(request, 'groups/lista.html', {'grupos': grupos})

def ver_grupo(request, id):
    grupo = get_object_or_404(Group, id=id)
    return render(request, 'groups/ver.html', {'grupo': grupo})

@login_required
def editar_grupo(request, id):
    grupo = get_object_or_404(Group, id=id)

    if grupo.owner != request.user:
        return redirect('core:home')

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=grupo)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.save()
            form.save_m2m()

            # Actualizar miembros con exclusividad
            miembros = form.cleaned_data.get('members', [])
            grupo.members.clear()
            for artista in miembros:
                if not Group.objects.filter(members=artista).exclude(id=grupo.id).exists():
                    grupo.members.add(artista)

            return redirect('groups:mis_grupos')
    else:
        form = GroupForm(instance=grupo)

    return render(request, 'groups/editar.html', {'form': form, 'grupo': grupo})

@login_required
def mis_grupos(request):
    if request.user.role != 'group_admin':
        return redirect('core:home')

    grupos = Group.objects.filter(owner=request.user)
    return render(request, 'groups/mis_grupos.html', {'grupos': grupos})