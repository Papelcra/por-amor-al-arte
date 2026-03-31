from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import GroupForm
from .models import Group


# 👥 CREAR GRUPO
@login_required
def crear_grupo(request):

    # 🔒 Solo admin de agrupación
    if request.user.role != 'group_admin':
        return redirect('core:home')

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)

        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()

            form.save_m2m()

            # 🔥 Validación: artista solo en un grupo
            miembros = form.cleaned_data.get('members')
            group.members.clear()

            for artista in miembros:
                if not Group.objects.filter(members=artista).exists():
                    group.members.add(artista)

            return redirect('groups:mis_grupos')

    else:
        form = GroupForm()

    return render(request, 'groups/crear.html', {'form': form})


# 📋 LISTA DE GRUPOS
def lista_grupos(request):
    grupos = Group.objects.all()
    return render(request, 'groups/lista.html', {'grupos': grupos})


# 🔍 VER GRUPO
def ver_grupo(request, group_id):
    grupo = get_object_or_404(Group, id=group_id)
    return render(request, 'groups/ver_grupo.html', {
        'grupo': grupo
    })


# ✏️ EDITAR GRUPO
def editar_grupo(request, group_id):
    grupo = get_object_or_404(Group, id=group_id)

    # 🔒 Seguridad: solo el dueño puede editar
    if grupo.owner != request.user:
        return redirect('lista_grupos')

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=grupo)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.owner = request.user
            grupo.save()
            form.save_m2m()
            return redirect('groups:ver_grupo', group_id=grupo.id)
    else:
        form = GroupForm(instance=grupo)

    return render(request, 'groups/editar_grupo.html', {
        'form': form,
        'grupo': grupo
    })

# 📂 MIS GRUPOS
@login_required
def mis_grupos(request):

    # 🔒 Solo admin de agrupación
    if request.user.role != 'group_admin':
        return redirect('core:home')

    grupos = Group.objects.filter(owner=request.user)

    return render(request, 'groups/mis_grupos.html', {
        'grupos': grupos
    })