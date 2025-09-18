# Главная функция
def two_sum(nums, target):
  # Проверки
  if not isinstance(nums, list):
    return None
  if len(nums) < 2:
    return None
  if not (isinstance(target, int) or (isinstance(target, float) and target.is_integer())):
    return None
  if not all(isinstance(item, int) or (isinstance(item, float) and item.is_integer()) for item in nums):
    return None

  # Алгоритм поиска двух подходящих чисел
  for i in range(len(nums) - 1):
    for j in range(i + 1, len(nums)):
      if nums[i] + nums[j] == target:
        return [i, j]

  # Если решение не найдено, возвращет None
  return None