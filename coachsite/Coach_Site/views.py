from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import Coach, Comment, Chat, AvailableSlot, TrainingSession
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required


from .forms import (
    CommentModelForm,
    CommentEditForm,
    UserEditForm,
    CoachEditForm,
    CustomUserCreationForm,
    MessageForm,
    AvailableSlotForm,
)

User = get_user_model()


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("my_profile"))
    else:
        form = CustomUserCreationForm()

    return render(request, "Coach_Site/register.html", {"form": form})


# Create your views here.
def index(request):
    data = Coach.objects.all()
    context = {"coachs": data}
    return render(request, "Coach_Site/home.html", context=context)


@login_required  # Требуем аутентификацию для просмотра профиля
def my_profile(request):
    user = request.user
    if user.is_coach:
        coach_data = get_object_or_404(Coach, pk=user)
        context = {"user": coach_data}
    else:
        context = {"user": request.user}

    return render(request, "Coach_Site/my_profile.html", context)


@login_required
def coach_detail(request, coach_id):
    user = request.user
    coach = get_object_or_404(Coach, pk=coach_id)
    comments = coach.comment_set.all()
    available_slots = AvailableSlot.objects.filter(coach=coach).order_by("start_time")
    available_slots = [
        slot for slot in available_slots if not slot.overlaps_with_training_session()
    ]  # Получаем доступные слоты
    context = {
        "coach": coach,
        "comments": comments,
        "user": user,
        "available_slots": available_slots,
    }  # Передаем слоты в шаблон
    return render(request, "Coach_Site/coach_detail.html", context)


@login_required  # Требуем аутентификацию пользовател
def add_comment(request, coach_id):
    coach_data = get_object_or_404(Coach, pk=coach_id)
    user = request.user
    if request.method == "POST":
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect(reverse("coach_detail", kwargs={"coach_id": coach_data.pk}))
    else:
        form = CommentModelForm()
    context = {
        "form": form,
        "title": "Добавление комментария",
        "id": coach_data.user.id,
    }
    return render(request, "Coach_Site/add_comment.html", context=context)


def user_comments(request):
    user = request.user
    comments = request.user.comment_set.all()
    context = {"user": user, "comments": comments}
    return render(request, "Coach_Site/my_profile_comments.html", context=context)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(
        Comment, pk=comment_id, author=request.user
    )  # Проверяем автора
    if request.method == "POST":
        form = CommentEditForm(
            request.POST, instance=comment
        )  # Передаем instance=comment
        if form.is_valid():
            form.save()  # Сохраняем измененный комментарий
            return redirect(
                reverse("coach_detail", kwargs={"coach_id": comment.coach.pk})
            )  # Вернуться к тренеру
    else:
        form = CommentEditForm(
            instance=comment
        )  # Инициализируем форму существующими данными

    context = {
        "form": form,
        "comment": comment,  # Передаем comment в контекст
        "title": "Редактирование комментария",
    }
    return render(request, "Coach_Site/edit_comment.html", context=context)


@login_required
def edit_profile(request):
    user = request.user
    coach = getattr(user, "coach", None)  # Пытаемся получить профиль тренера

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=user)
        if coach:
            coach_form = CoachEditForm(request.POST, instance=coach)
        else:
            coach_form = (
                None  # Не отображаем и не обрабатываем форму тренера, если его нет
            )

        if user_form.is_valid():
            user_form.save()

            if (
                coach and coach_form and coach_form.is_valid()
            ):  # Проверяем существует ли форма
                coach_form.save()  # Сохраняем изменения тренера

            return redirect(reverse("my_profile"))
    else:
        user_form = UserEditForm(instance=user)
        if coach:
            coach_form = CoachEditForm(instance=coach)
        else:
            coach_form = None

    context = {
        "user_form": user_form,
        "coach_form": coach_form,  # Может быть None
    }
    return render(request, "Coach_Site/edit_profile.html", context)


@login_required
def register_as_coach(request):
    if hasattr(request.user, "coach_profile"):  # Проверяем, есть ли уже профиль тренера
        # Пользователь уже зарегистрирован как тренер
        return redirect("my_profile")  # Перенаправляем на профиль

    if request.method == "POST":
        form = CoachEditForm(request.POST)
        if form.is_valid():
            coach = form.save(commit=False)
            coach.user = request.user  # Связываем тренера с текущим пользователем
            coach.save()
            return redirect("my_profile")  # Перенаправляем на профиль
    else:
        form = CoachEditForm()

    context = {"form": form, "title": "Регистрация тренера"}
    return render(request, "Coach_Site/register_as_coach.html", context)


@login_required
def start_chat(request, coach_id):
    """Начинает чат с тренером."""
    coach = get_object_or_404(Coach, pk=coach_id)
    chat, created = Chat.objects.get_or_create(
        user=request.user, coach=coach
    )  # Получаем существующий чат или создаем новый
    return redirect(reverse("chat_detail", kwargs={"chat_id": chat.pk}))


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user == chat.user:
        opponent_name = chat.coach.user.username
        user_type = "user"
    else:
        opponent_name = chat.user.username
        user_type = "coach"
    context = {"chat": chat, "opponent_name": opponent_name, "user_type": user_type}
    return render(request, "Coach_Site/chat_detail.html", context)


@login_required
def chat_list(request):
    chats = []
    if hasattr(request.user, "coach"):
        # Если пользователь - тренер, показываем чаты, где он - тренер
        chats = Chat.objects.filter(coach=request.user.coach)
    else:
        # Если пользователь - не тренер, показываем чаты, где он - пользователь
        chats = Chat.objects.filter(user=request.user)
    return render(request, "Coach_Site/chat_list.html", {"chats": chats})


@login_required
def coach_schedule(request):
    coach = Coach.objects.get(
        user=request.user
    )  # Предполагаем, что у пользователя есть профиль Coach
    slots = AvailableSlot.objects.filter(coach=coach).order_by("start_time")
    training_sessions = TrainingSession.objects.filter(coach=coach).order_by(
        "slot__start_time"
    )
    slots = [
        slot for slot in slots if not slot.overlaps_with_training_session()
    ]  # Получаем тренировки
    form = AvailableSlotForm()
    if request.method == "POST":
        form = AvailableSlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.coach = coach
            slot.save()
            return redirect("coach_schedule")
    return render(
        request,
        "Coach_Site/coach_schedule.html",
        {
            "slots": slots,
            "form": form,
            "training_sessions": training_sessions,
        },
    )


@login_required
def book_training(request, slot_id):
    slot = get_object_or_404(AvailableSlot, id=slot_id)
    coach = slot.coach
    TrainingSession.objects.create(user=request.user, coach=coach, slot=slot)
    return redirect("user_schedule")  # Редирект на страницу пользователя с его записями


@login_required
def user_schedule(request):
    sessions = TrainingSession.objects.filter(user=request.user).order_by(
        "slot__start_time"
    )
    print(sessions)
    return render(request, "Coach_Site/user_schedule.html", {"sessions": sessions})


@login_required
def coach_training_requests(request):
    coach = Coach.objects.get(user=request.user)
    training_requests = TrainingSession.objects.filter(
        coach=coach, status="pending"
    ).order_by("slot__start_time")
    return render(
        request,
        "Coach_Site/coach_training_requests.html",
        {"training_requests": training_requests},
    )


@login_required
def confirm_training(request, session_id):
    print(session_id)
    session = get_object_or_404(
        TrainingSession, id=session_id, coach__user=request.user
    )
    session.status = "confirmed"
    session.save()

    messages.success(request, "Тренировка успешно подтверждена!")
    return redirect("coach_training_requests")


@login_required
def reject_training(request, session_id):
    session = get_object_or_404(
        TrainingSession, id=session_id, coach__user=request.user
    )
    session.status = "rejected"
    session.save()
    return redirect("coach_training_requests")
