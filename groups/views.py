from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import GroupForm
from .models import Group
from artists.models import Artist



def crear_grupo(request):
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES)

        # 🔥 obtenemos los miembros correctamente
        selected_members = request.POST.getlist('members')

        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.save()

            # 🔥 guardamos relación many-to-many
            grupo.members.set(selected_members)

            return redirect('artists:lista_artistas')
    else:
        form = GroupForm()
        selected_members = []

    return render(request, 'artists/crear_grupo.html', {
        'form': form,
        'selected_members': selected_members
    })


# 📋 LISTA DE GRUPOS
def lista_grupos(request):
    grupos = Group.objects.all()
    return render(request, 'groups/lista.html', {'grupos': grupos})


# 🔍 VER GRUPO
def ver_grupo(request, group_id):
    grupo = get_object_or_404(Group, id=group_id)

    # 🔥 usar relación consistente
    miembros = grupo.members.all()

    return render(request, 'groups/ver_grupo.html', {
        'grupo': grupo,
        'miembros': miembros
    })


# ✏️ EDITAR GRUPO
def editar_grupo(request, group_id):
    grupo = get_object_or_404(Group, id=group_id)

    if grupo.owner != request.user:
        return redirect('groups:lista_grupos')

    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=grupo)

        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.save()

            miembros_seleccionados = form.cleaned_data.get('members', [])

            # 🔥 1. quitar grupo a los que ya no están
            for artista in Artist.objects.filter(group=grupo):
                if artista not in miembros_seleccionados:
                    artista.group = None
                    artista.save()

            # 🔥 2. asignar grupo a los seleccionados
            for artista in miembros_seleccionados:
                artista.group = grupo
                artista.save()

            # 🔥 3. sincronizar ManyToMany
            grupo.members.set(miembros_seleccionados)

            messages.success(request, "✅ Grupo actualizado correctamente")
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
    if request.user.role != 'group_admin':
        return redirect('core:home')

    grupos = Group.objects.filter(owner=request.user)

    return render(request, 'groups/mis_grupos.html', {
        'grupos': grupos
    })